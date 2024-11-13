from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from . import serializers

User = get_user_model()

class FilteredUserViewSet(UserViewSet):

    queryset = User.objects.prefetch_related('groups')
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'post']