from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('dishes', views.DishViewSet)
# router.register('dish-images', views.DishImageViewSet)
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('carts', views.CartViewSet, basename='carts')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='carts')
cart_router.register('cart-items', views.CartItemViewSet, basename='cart-items')

router.register('tables', views.TableViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)
# router.register('bill', views.BillViewSet)

table_router = routers.NestedDefaultRouter(router, 'tables', lookup='tables')
table_router.register('bill', views.BillViewSet, basename='bill')

# order_router = routers.NestedDefaultRouter(router, 'orders', lookup='orders')
# order_router.register('order-items', views.OrderItemViewSet, basename='order-items')

urlpatterns = router.urls + cart_router.urls + table_router.urls