from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Dish)
admin.site.register(models.Table)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Bill)
admin.site.register(models.Promotion)
admin.site.register(models.PromotionItem)