from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('dishes', views.DishViewSet)
# router.register('dish-images', views.DishImageViewSet)
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('carts', views.CartViewSet, basename='carts')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='carts')
cart_router.register('cart-items', views.CartItemViewSet, basename='cart-items')

# router.register('tables', views.TableViewSet)
# router.register('orders', views.OrderViewSet)
# router.register('order-items', views.OrderItemViewSet)
# router.register('bills', views.BillViewSet)

urlpatterns = router.urls + cart_router.urls