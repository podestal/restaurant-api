from django.utils import timezone
from datetime import time
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from .permissions import IsAdminOrWaiter
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
# from channels.layers import get_channel_layer
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

    queryset = models.Table.objects.prefetch_related('orders')
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateTableSerializer    
        return serializers.GetTableSerializer
    
class BillViewSet(ModelViewSet):

    queryset = models.Bill.objects.select_related('table').prefetch_related('order_items__dish')
    permission_classes = [IsAdminOrWaiter]

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
    http_method_names = ['post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderItemSerializer
        return serializers.GetOrderItemSerializer
