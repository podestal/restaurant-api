from djoser.serializers import UserSerializer as BasedUserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group

class UserSerializer(BasedUserSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Group.objects.all()
    )

    class Meta(BasedUserSerializer.Meta):
        fields = ["id", "first_name", "last_name", "username", "email", 'groups']

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email", "first_name", "last_name"]
