from rest_framework import serializers
from . import models

class GetDishSerializer(serializers.ModelSerializer):

    picture_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'cost', 'created_at', 'available', 'picture_url', 'category', 'discount', 'final_price']

    def get_picture_url(self, obj):
        request = self.context.get('request')
        if obj.picture:
            return request.build_absolute_uri(obj.picture.url)
        return None


class CreateDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'cost', 'available', 'picture', 'category', 'discount']

class UpdateDishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'description', 'cost', 'available', 'picture', 'category', 'discount']

class GetCategorySerializer(serializers.ModelSerializer):

    available = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description', 'time_period', 'available']

    def get_available(self, obj):
        dish_count = models.Dish.objects.select_related('category').filter(category=obj, available=True).count()
        return dish_count > 0

class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description']

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'dish', 'promotion', 'price', 'cart', 'observations']

class SimpleCartItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    dish_id = serializers.SerializerMethodField()
    promotion_id = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'quantity', 'name', 'price', 'dish_id', 'promotion_id', 'picture', 'observations']

    def get_name(self, obj):
        if obj.dish:
            return obj.dish.name
        return obj.promotion.name if obj.promotion else None

    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.dish and obj.dish.picture:
            return request.build_absolute_uri(obj.dish.picture.url)
        return None
    
    def get_dish_id(self, obj):
        return obj.dish.id if obj.dish else None
    
    def get_promotion_id(self, obj):
        return obj.promotion.id if obj.promotion else None

class CartSerializer(serializers.ModelSerializer):

    items = SimpleCartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = ['id', 'session_id', 'created_at', 'updated_at', 'user', 'items']

class GetPromotionItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta: 
        model = models.PromotionItem
        fields = ['id', 'quantity', 'name']

    def get_name(self, obj):
        return obj.dish.name if obj.dish else None

class GetPromotionSerializer(serializers.ModelSerializer):

    items = GetPromotionItemSerializer(many=True)

    class Meta:
        model = models.Promotion
        fields = ['id', 'name', 'description', 'amount', 'is_active', 'items']

class GetSimplePromotionSerializer(serializers.ModelSerializer):

    items = GetPromotionItemSerializer(many=True)

    class Meta:
        model = models.Promotion
        fields = ['id', 'name', 'items']

class SimpleOrderItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    promotion = GetSimplePromotionSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'quantity', 'cost', 'observations', 'name', 'created_at', 'category_name', 'promotion']

    def get_name(self, obj):
        if obj.dish:
            return obj.dish.name if obj.dish else None
        return obj.promotion.name if obj.promotion else None

    def get_promotion_name(self, obj):
        return obj.promotion.name if obj.promotion else None

    
    def get_category_name(self, obj):
        if obj.dish:
            return f'{obj.dish.category.name}' if obj.dish.category.name else None
        return None

class GetOrderSerializer(serializers.ModelSerializer):

    order_items = SimpleOrderItemSerializer(many=True)
    waiter = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = ['id', 'status', 'order_items', 'waiter', 'updated_at', 'order_type', 'customer_name', 'customer_phone', 'customer_email', 'customer_address']

    def get_waiter(self, obj):
        return f'{obj.created_by.first_name} {obj.created_by.last_name[0]}' if obj.created_by else None

class GetBillSerializer(serializers.ModelSerializer):

    order_items = SimpleOrderItemSerializer(many=True)

    class Meta:
        model = models.Bill
        fields = ['id', 'order_items', 'table', 'document']

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
        fields = ['id', 'table', 'created_by', 'status', 'order_type']

class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'table', 'status', 'order_type']

    def create(self, validated_data):
        user = self.context['user_id']
        if user:
            return models.Order.objects.create(created_by=user, **validated_data)
        return models.Order.objects.create(**validated_data)

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
        fields = ['id', 'dish', 'order', 'quantity', 'observations', 'cost', 'bill', 'promotion']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = ['id', 'order', 'amount', 'stripe_payment_intent_id', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'stripe_payment_intent_id', 'status', 'created_at', 'updated_at']

class CreatePromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Promotion
        fields = ['id', 'name', 'description', 'amount', 'is_active']


class CreatePromotionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PromotionItem
        fields = ['id', 'promotion', 'dish', 'quantity']

class DiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DiscountCode
        fields = '__all__'
    