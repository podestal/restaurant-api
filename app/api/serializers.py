from rest_framework import serializers
from . import models

class GetDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'cost', 'created_at', 'available', 'picture', 'category']


class CreateDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'cost', 'available', 'picture', 'category']

class UpdateDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'cost', 'available', 'picture', 'category']

# class CreateDishImageSerializer(serializers.ModelSerializer):

#     class Meta: 
#         model = models.DishImage
#         fields = ['id', 'image', 'dish']

class GetCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description', 'time_period']

class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description', 'time_period']

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'dish', 'price', 'cart']

class SimpleCartItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'name', 'picture', 'price']

    def get_name(self, obj):
        return obj.dish.name if obj.dish else None

    def get_picture(self, obj):
        return obj.dish.picture if obj.dish else None

class CartSerializer(serializers.ModelSerializer):

    items = SimpleCartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = ['id', 'session_id', 'created_at', 'updated_at', 'user', 'items']

class GetOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'table', 'created_at', 'updated_at', 'status', 'created_by']

class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'table', 'status']

    def create(self, validated_data):
        user = self.context['user_id']
        return models.Order.objects.create(created_by=user, **validated_data)

class GetTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Table
        fields = ['id', 'number', 'is_available', 'orders', 'bill']

    

class CreateTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Table
        fields = ['id', 'number', 'is_available']


class GetOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ['id', 'dish', 'order', 'quantity', 'observations', 'table', 'bill', 'created_at', 'cost']

class CreateOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ['id', 'dish', 'order', 'quantity', 'observations', 'table', 'bill', 'cost']

class GetBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bill
        fields = ['id', 'table']

class CreateBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bill
        fields = ['id', 'table']