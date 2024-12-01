from django.utils import timezone
from datetime import datetime, time
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
from .permissions import IsAdminOrWaiter
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .utils import send_order_status_email

from . import serializers
from . import models

import stripe
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class DishViewSet(ModelViewSet):

    queryset = models.Dish.objects.select_related('category').order_by('id')
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):

        if self.request.method == 'POST':
            return serializers.CreateDishSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateDishSerializer
        return serializers.GetDishSerializer

    
class CategoryViewSet(ModelViewSet):

    queryset = models.Category.objects.order_by('id')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateCategorySerializer
        return serializers.GetCategorySerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class CartViewSet(ModelViewSet):

    serializer_class = serializers.CartSerializer
    http_method_names = ['get']
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):

        session_id = self.request.headers.get('Session-ID')
    
        if not session_id:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key

        models.Cart.objects.get_or_create(session_id=session_id)

        return models.Cart.objects.filter(session_id=session_id).prefetch_related('items__dish')
    
    @action(detail=False, methods=["get"], url_path='my-cart', permission_classes=[permissions.IsAuthenticated])
    def get_cart_for_authenticated_user(self, request):
        user = self.request.user
        cart, created = models.Cart.objects.get_or_create(user=user)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    

    
class CartItemViewSet(ModelViewSet):

    queryset = models.CartItem.objects.select_related('dish', 'cart').prefetch_related('dish').order_by('id')
    serializer_class = serializers.CartItemSerializer

    
class TableViewSet(ModelViewSet):

    queryset = models.Table.objects.prefetch_related('orders').order_by('id')
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateTableSerializer    
        return serializers.GetTableSerializer
    
class BillViewSet(ModelViewSet):

    queryset = models.Bill.objects.select_related('table').prefetch_related('order_items__dish')
    permission_classes = [IsAdminOrWaiter]

    def get_serializer_context(self):
        return {'table_id': self.kwargs.get('tables_pk')}

    def get_serializer_class(self):

        if self.request.method == 'POST':   
            return serializers.CreateBillSerializer
        return serializers.GetBillSerializer
    
    def get_queryset(self):
        table_id = self.kwargs.get('tables_pk')
        return self.queryset.filter(table_id=table_id)
    
class OrderViewSet(ModelViewSet):

    queryset = models.Order.objects.select_related('table', 'created_by').prefetch_related('order_items__dish').order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['table', 'status']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):

        cart_id = request.query_params.get('cart')
        table= request.data.get('table')
        created_by = request.data.get('created_by')
        customer_name = request.data.get('customer_name')
        customer_phone = request.data.get('customer_phone')
        customer_address = request.data.get('customer_address')
        customer_email = request.data.get('customer_email')
        status = request.data.get('status')
        order_type = request.data.get('order_type')

        order = models.Order.objects.create(
            table_id=table, 
            created_by_id=created_by, 
            status=status,
            order_type=order_type,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            customer_email=customer_email,
            *args,
            **kwargs)
        
        if cart_id:

            cart = models.Cart.objects.prefetch_related('items').get(id=cart_id)
            for item in cart.items.all():
                models.OrderItem.objects.create(
                    order=order,
                    dish=item.dish,
                    cost=item.price,
                    quantity=item.quantity,
                    observations=item.observations,
                )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "order_status_updates",
                {
                    "type": "send_order_status_update",
                    "message": {
                        "order_id": order.id,
                    },
                },
            )

            cart.items.all().delete()

        return Response(serializers.CreateOrderSerializer(order).data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        order = self.get_object()

        email = request.query_params.get('email')

        if email and order.status == 'C':
            send_order_status_email(email, order)

        if order.status in ['S', 'C']: 
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "order_status_updates",
                {
                    "type": "send_order_status_update",
                    "message": {
                        "order_id": order.id,
                        "status": order.status,
                    },
                },
            )
        return response

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.UpdateOrderSerializer
        return serializers.GetOrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user}

class OrderItemViewSet(ModelViewSet):

    queryset = models.OrderItem.objects.select_related('order', 'dish').prefetch_related('order__table', 'dish__category').order_by('created_at')
    permission_classes = [IsAdminOrWaiter]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderItemSerializer
        return serializers.GetOrderItemSerializer
    
    @action(detail=False, methods=['get'])
    def by_month(self, request):
        """
        Get OrderItems filtered by the specified month and year.
        """

        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            today = datetime.today()
            month = today.month
            year = today.year
        else:
            
            month = int(month)
            year = int(year)

        order_items = self.queryset.filter(created_at__year=year, created_at__month=month)
        serializer = serializers.SimpleOrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

class ProcessPaymentView(APIView):
    def post(self, request, *args, **kwargs):

        try:
            amount = request.data.get("amount")
            payment_method_id = request.data.get("payment_method_id")

            if not amount or not payment_method_id:
                return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency="usd",
                payment_method=payment_method_id,
                confirm=True, 
                metadata={"order_id": "12345"}, 
            )

            return Response({
                "message": "Payment successful",
                "payment_intent": payment_intent,
            })

        except stripe.error.CardError as e:
            return Response({"error": e.error.message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
