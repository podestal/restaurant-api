from django.utils import timezone
from datetime import datetime, time
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from .permissions import IsAdminOrWaiter
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from . import serializers
from . import models

class DishViewSet(ModelViewSet):

    queryset = models.Dish.objects.select_related('category')
    
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

    queryset = models.CartItem.objects.select_related('dish', 'cart').prefetch_related('dish')
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
    permission_classes = [IsAdminOrWaiter]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        # Broadcast status change if status is "Served"
        order = self.get_object()
        if order.status == 'S':  # "Served"
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "order_status_updates",
                {
                    "type": "send_order_status_update",
                    "message": {
                        "order_id": order.id,
                        "status": order.status,
                        "table": order.table.id,
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

    queryset = models.OrderItem.objects.select_related('order', 'dish').prefetch_related('order__table', 'dish__category')
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
