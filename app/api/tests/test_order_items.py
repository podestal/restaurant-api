# import pytest
# from rest_framework import status
# from model_bakery import baker
# from api.models import Order, Table, OrderItem, Dish
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# User = get_user_model()

# @pytest.fixture
# def dish():
#     """Fixture to create a Dish instance."""
#     return baker.make(Dish)

# @pytest.fixture
# def order(create_order):
#     """Fixture to create an Order instance."""
#     return create_order

# @pytest.fixture
# def create_order_item(order, dish):
#     """Fixture to create an OrderItem instance."""
#     return baker.make(OrderItem, order=order, dish=dish, quantity=2, cost=15.50)

# @pytest.mark.django_db
# class TestOrderItemViewSet:
#     """Test class for OrderItem model and OrderItemViewSet."""

#     def test_create_order_item_unauthenticated_return_401(self, api_client, order, dish):
#         """Test unauthenticated access for creating an OrderItem."""
#         data = {
#             'order': order.id,
#             'dish': dish.id,
#             'quantity': 2,
#             'cost': 15.50,
#             'observations': 'Extra spicy'
#         }
#         response = api_client.post('/api/order-items/', data)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_create_order_item_authenticated_return_403(self, authenticated_user, order, dish):
#         """Test creating an OrderItem with authenticated user without permission."""
#         data = {
#             'order': order.id,
#             'dish': dish.id,
#             'quantity': 2,
#             'cost': 15.50,
#             'observations': 'Extra spicy'
#         }
#         response = authenticated_user.post('/api/order-items/', data)
#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_create_order_item_waiter_user_return_201(self, waiter_user, order, dish):
#         """Test creating an OrderItem with a waiter user."""
#         data = {
#             'order': order.id,
#             'dish': dish.id,
#             'quantity': 2,
#             'cost': 15.50,
#             'observations': 'Extra spicy'
#         }
#         response = waiter_user.post('/api/order-items/', data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['order'] == order.id
#         assert response.data['dish'] == dish.id
#         assert response.data['quantity'] == 2
#         assert response.data['cost'] == '15.50'

#     def test_get_order_item_list_unauthenticated_return_401(self, api_client, create_order_item):
#         """Test retrieving a list of OrderItems without authentication."""
#         response = api_client.get('/api/order-items/')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_get_order_item_list_authenticated_return_403(self, authenticated_user, create_order_item):
#         """Test retrieving a list of OrderItems with an authenticated user without permission."""
#         response = authenticated_user.get('/api/order-items/')
#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_get_order_item_list_waiter_return_200(self, waiter_user, create_order_item):
#         """Test retrieving a list of OrderItems with a waiter user."""
#         response = waiter_user.get('/api/order-items/')
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]['id'] == create_order_item.id

#     def test_get_order_item_detail_unauthenticated_user_return_401(self, api_client, create_order_item):
#         """Test retrieving a single OrderItem detail without authentication."""
#         response = api_client.get(f'/api/order-items/{create_order_item.id}/')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_get_order_item_detail_authenticated_return_403(self, authenticated_user, create_order_item):
#         """Test retrieving a single OrderItem detail with an authenticated user without permission."""
#         response = authenticated_user.get(f'/api/order-items/{create_order_item.id}/')
#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_update_order_item_unauthenticated_return_401(self, api_client, create_order_item):
#         """Test updating an OrderItem without authentication."""
#         data = {'quantity': 5}
#         response = api_client.patch(f'/api/order-items/{create_order_item.id}/', data)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_update_order_item_authenticated_return_403(self, authenticated_user, create_order_item):
#         """Test updating an OrderItem with an authenticated user without permission."""
#         data = {'quantity': 5}
#         response = authenticated_user.patch(f'/api/order-items/{create_order_item.id}/', data)
#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_delete_order_item_unauthenticated_return_401(self, api_client, create_order_item):
#         """Test deleting an OrderItem without authentication."""
#         response = api_client.delete(f'/api/order-items/{create_order_item.id}/')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_delete_order_item_authenticated_return_403(self, authenticated_user, create_order_item):
#         """Test deleting an OrderItem with an authenticated user without permission."""
#         response = authenticated_user.delete(f'/api/order-items/{create_order_item.id}/')
#         assert response.status_code == status.HTTP_403_FORBIDDEN
