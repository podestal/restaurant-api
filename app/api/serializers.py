from rest_framework import serializers
from . import models

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = [ 'name']

class GetDishSerializer(serializers.ModelSerializer):

    category = CategoryNameSerializer()

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