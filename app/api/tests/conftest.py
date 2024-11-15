import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from core.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from api.models import Order, OrderItem


@pytest.fixture
def api_client():
    """Fixture to provide APIClient instance."""
    return APIClient()


@pytest.fixture
def create_user():
    """Fixture to create a normal user."""
    return baker.make(User)


@pytest.fixture
def create_admin_user():
    """Fixture to create an admin user."""
    return baker.make(User, is_staff=True)


@pytest.fixture
def authenticated_user(api_client, create_user):
    """Fixture to authenticate a normal user."""
    api_client.force_authenticate(user=create_user)
    return api_client

# @pytest.fixture
# def waiter_user(api_client, create_user):
#     """Fixture to create a user with 'waiter' permissions."""
#     order_content_type = ContentType.objects.get_for_model(Order)
#     order_item_content_type = ContentType.objects.get_for_model(OrderItem)
#     permissions =  Permission.objects.filter(
#         content_type__in = [order_content_type, order_item_content_type],
#         codename__in = ["add_order", "change_order", "delete_order", "view_order",
#             "add_order_item", "change_order_item", "delete_order_item", "view_order_item"
#         ]
#     )

#     waiter_group.permissions.set(permissions)

#     user = baker.make(User)
#     user.groups.add(waiter_group)
#     api_client.force_authenticate(user=user)
    
#     return api_client

#     create_user.user_permissions.set(permissions)
#     api_client.force_authenticate(user=create_user)
#     return api_client


@pytest.fixture
def admin_user(api_client, create_admin_user):
    """Fixture to authenticate an admin user."""
    api_client.force_authenticate(user=create_admin_user)
    return api_client
