from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()

router.register('dishes', views.DishViewSet)

router.register('categories', views.CategoryViewSet, basename='categories')
router.register('carts', views.CartViewSet, basename='carts')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='carts')
cart_router.register('cart-items', views.CartItemViewSet, basename='cart-items')

router.register('tables', views.TableViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)

table_router = routers.NestedDefaultRouter(router, 'tables', lookup='tables')
table_router.register('bill', views.BillViewSet, basename='bill')

router.register('promotions', views.PromotionViewSet, basename='promotions')
router.register('discounts', views.DiscountCodeViewSet, basename='discounts')

urlpatterns = [
    path('process-payment/', views.ProcessPaymentView.as_view(), name='process-payment'),
]


urlpatterns += router.urls + cart_router.urls + table_router.urls