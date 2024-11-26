from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register("users", views.FilteredUserViewSet, basename="users")

urlpatterns = router.urls