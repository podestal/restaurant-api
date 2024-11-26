from datetime import timedelta, timezone
from django.conf import settings
from django.db import models

class Category(models.Model):

    MORNING = 'M'
    EVENING = 'E'
    BOTH = 'B'

    TIME_PERIODS = [
        (MORNING, 'Morning'),
        (EVENING, 'Evening'),
        (BOTH, 'Both'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    time_period = models.CharField(max_length=1, choices=TIME_PERIODS, default=BOTH)

    def __str__(self):
        return self.name

class Dish(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="dishes/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
class Cart(models.Model):

    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.session_id or "No Session ID"
    
    def is_expired(self):
        expiry_duration = timedelta(hours=24)
        return timezone.now() > self.updated_at + expiry_duration
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,  related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.dish.name}"
    
# class DishImage(models.Model):

#     dish = models.OneToOneField(Dish, on_delete=models.CASCADE, related_name='image')
#     image = models.ImageField(upload_to='dishes/')

class Table(models.Model):

    TABLE_VACANT = 'V'
    TABLE_OCCUPIED = 'O'
    TABLE_RESERVED = 'R'

    TABLE_STATUS_OPTIONS = [
        (TABLE_VACANT, 'Vacant'),
        (TABLE_OCCUPIED, 'Occupied'),
        (TABLE_RESERVED, 'Reserved'),
    ]

    number = models.CharField(max_length=5, unique=True)
    status = models.CharField(max_length=10, choices=TABLE_STATUS_OPTIONS, default=TABLE_VACANT)
    guest_name = models.CharField(max_length=50, blank=True, null=True)
    seats = models.IntegerField(default=2)


    def __str__(self):
        return f'Table {self.number}'
    
class Bill(models.Model):

    table = models.OneToOneField(Table, on_delete=models.CASCADE, related_name='bill')


    def save(self, *args, **kwargs):
        """Create or update a bill, updating table status"""
        self.table.status = Table.TABLE_OCCUPIED
        self.table.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        """Delete the bill, updating table status"""
        self.table.status = Table.TABLE_VACANT
        self.table.save()
        super().delete(*args, **kwargs)

    
class Order(models.Model):

    PENDING_DISH = 'P'
    SERVED_DISH = 'S'
    COMPLETED_DISH = 'C'

    ORDER_STATUS_OPTIONS = [
        (PENDING_DISH, 'Pending'),
        (SERVED_DISH, 'Served'),
        (COMPLETED_DISH, 'Completed')
    ]

    DINE_IN_TYPE = 'I'
    DELIVERY_TYPE = 'D'
    TAKE_OUT_TYPE = 'T'

    ORDER_TYPE_OPTIONS = [
        (DINE_IN_TYPE, 'Dine in'),
        (DELIVERY_TYPE, 'Delivery'),
        (TAKE_OUT_TYPE, 'Take out'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_OPTIONS, max_length=1, default=PENDING_DISH)
    order_type = models.CharField(choices=ORDER_TYPE_OPTIONS, max_length=1, default=DINE_IN_TYPE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)
    customer_address = models.TextField(null=True, blank=True) 
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
