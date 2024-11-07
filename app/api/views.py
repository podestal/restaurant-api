from django.utils import timezone
from datetime import time
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from . import serializers
from . import models

class DishViewSet(ModelViewSet):

    queryset = models.Dish.objects.select_related('category')
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
    
# class DishImageViewSet(ModelViewSet):

#     queryset = models.DishImage.objects.select_related('dish')
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['dish']

#     def get_permissions(self):
#         if self.request.method in ['GET']:
#             return [permissions.AllowAny()]
#         return [permissions.IsAdminUser()]

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return serializers.CreateDishImageSerializer
#         return serializers.GetDishImageSerializer
    
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

    # def get_queryset(self):

    #     current_time = timezone.localtime().time()
    #     morning_start = time(11, 0)
    #     morning_end = time(18, 0)
    #     night_start = time (19, 0)
    #     night_end = time(23, 30)

    #     if (self.request.user.is_anonymous):
    #         if morning_start <= current_time < morning_end:
    #             return models.Category.objects.filter(time_period__in=[models.Category.MORNING])
    #         if night_start <= current_time < night_end:
    #             return models.Category.objects.filter(time_period__in=[models.Category.EVENING])
            
    #         return models.Category.objects.none()
        
    #     return models.Category.objects.all()

class CartViewSet(ModelViewSet):

    # queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    def get_queryset(self):

        session_id = self.request.session.session_key
        if not session_id:
            self.request.session.create()
            session_id = self.request.session.session_key

        models.Cart.objects.get_or_create(session_id=session_id)

        return models.Cart.objects.filter(session_id=session_id)
    
class CartItemViewSet(ModelViewSet):

    queryset = models.CartItem.objects.select_related('dish', 'cart')
    serializer_class = serializers.CartItemSerializer

    
class TableViewSet(ModelViewSet):

    queryset = models.Table.objects.prefetch_related('orders', 'bill')
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateTableSerializer    
        return serializers.GetTableSerializer
    
class OrderViewSet(ModelViewSet):

    queryset = models.Order.objects.select_related('table', 'created_by')
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['table', 'status']
    permission_classes = [permissions.IsAuthenticated]

    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     if 'status' in serializer.validated_data:
    #         channel_layer = get_channel_layer()
    #         async_to_sync(channel_layer.group_send)(
    #             "orders_group",
    #             {
    #                 "type": "order_status_update",
    #                 "message": f"Order {instance.id} status changed to {instance.get_status_display()}"
    #             }
    #         )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        return serializers.GetOrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user}

class OrderItemViewSet(ModelViewSet):

    queryset = models.OrderItem.objects.select_related('order', 'dish', 'table', 'bill')
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'table', 'bill', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderItemSerializer
        return serializers.GetOrderItemSerializer

class BillViewSet(ModelViewSet):

    queryset = models.Bill.objects.select_related('table')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['table']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return serializers.CreateBillSerializer
        return serializers.GetBillSerializer