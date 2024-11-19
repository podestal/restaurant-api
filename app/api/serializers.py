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
        fields = ['id', 'quantity', 'dish', 'price', 'cart', 'observations']

class SimpleCartItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    dish_id = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'name', 'picture', 'price', 'dish_id', 'observations']

    def get_name(self, obj):
        return obj.dish.name if obj.dish else None

    def get_picture(self, obj):
        return obj.dish.picture if obj.dish else None
    
    def get_dish_id(self, obj):
        return obj.dish.id if obj.dish else None

class CartSerializer(serializers.ModelSerializer):

    items = SimpleCartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = ['id', 'session_id', 'created_at', 'updated_at', 'user', 'items']

    #     class SimpleCartItemSerializer(serializers.ModelSerializer):

    # name = serializers.SerializerMethodField()
    # picture = serializers.SerializerMethodField()
    # dish_id = serializers.SerializerMethodField()

    # class Meta:
    #     model = models.CartItem
    #     fields = ['id', 'quantity', 'name', 'picture', 'price', 'dish_id', 'observations']

    # def get_name(self, obj):
    #     return obj.dish.name if obj.dish else None

    # def get_picture(self, obj):
    #     return obj.dish.picture if obj.dish else None
    
    # def get_dish_id(self, obj):
    #     return obj.dish.id if obj.dish else None

class SimpleOrderItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    # dish_id = serializers.SerializerMethodField()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'quantity', 'cost', 'observations', 'name']

    def get_name(self, obj):
        return obj.dish.name if obj.dish else None
    
    def get_dish_id(self, obj):
        return obj.dish.id if obj.dish else None

class GetOrderSerializer(serializers.ModelSerializer):

    order_items = SimpleOrderItemSerializer(many=True)
    waiter = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = ['id', 'status', 'order_items', 'waiter']

    def get_waiter(self, obj):
        return f'{obj.created_by.first_name} {obj.created_by.last_name[0]}' if obj.created_by else None

class GetBillSerializer(serializers.ModelSerializer):

    order_items = SimpleOrderItemSerializer(many=True)

    class Meta:
        model = models.Bill
        fields = ['id', 'order_items', 'table']

class CreateBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bill
        fields = ['id']

    def create(self, validated_data):
        table_id = self.context['table_id']
        return models.Bill.objects.create(table_id=table_id, **validated_data)

class UpdateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'table', 'created_by', 'status']

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
        fields = ['id', 'number', 'status', 'guest_name', 'seats']

    

class CreateTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Table
        fields = ['id', 'number', 'status', 'seats']


class GetOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ['id', 'quantity', 'observations', 'created_at', 'cost']

class CreateOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ['id', 'dish', 'order', 'quantity', 'observations', 'cost', 'bill']
