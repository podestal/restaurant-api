import pytest
from rest_framework import status
from model_bakery import baker
from api.models import Order, Table
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    """Fixture to create a User instance."""
    return baker.make(User)

@pytest.fixture
def table():
    """Fixture to create a Table instance."""
    return baker.make(Table)

@pytest.fixture
def create_order(user, table):
    """Fixture to create an Order instance."""
    return baker.make(Order, created_by=user, table=table, status=Order.PENDING_DISH)

@pytest.mark.django_db
class TestOrderViewSet:
    """Test class for Order model and OrderViewSet."""

    def test_create_order_unauthenticated_return_401(self, api_client, table):
        """Test creating an order."""
        data = {
            'table': table.id,
            'status': Order.PENDING_DISH
        }
        response = api_client.post('/api/orders/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_authenticated_return_403(self, authenticated_user, table):
        """Test creating an order."""
        data = {
            'table': table.id,
            'status': Order.PENDING_DISH
        }
        response = authenticated_user.post('/api/orders/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_order_admin_return_201(self, admin_user, table):
        """Test creating an order."""
        data = {
            'table': table.id,
            'status': Order.PENDING_DISH
        }
        response = admin_user.post('/api/orders/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['table'] == table.id
        assert response.data['status'] == Order.PENDING_DISH
        assert Order.objects.filter(id=response.data['id']).exists()

    def test_get_order_list_unauthenticated_return_401(self, api_client, create_order):
        """Test retrieving a list of orders."""
        response = api_client.get('/api/orders/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_order_list_authenticated_return_403(self, authenticated_user, create_order):
        """Test retrieving a list of orders."""
        response = authenticated_user.get('/api/orders/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_order_list_admin_return_200(self, admin_user, create_order):
        """Test retrieving a list of orders."""
        response = admin_user.get('/api/orders/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == create_order.id

    def test_get_order_detail_unauthenticated_user_return_401(self, api_client, create_order):
        """Test retrieving a single order detail."""
        response = api_client.get(f'/api/orders/{create_order.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_order_detail_admin_authenticated_return_403(self, authenticated_user, create_order):
        """Test retrieving a single order detail."""
        response = authenticated_user.get(f'/api/orders/{create_order.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_order_detail_admin_user_return_200(self, admin_user, create_order):
        """Test retrieving a single order detail."""
        response = admin_user.get(f'/api/orders/{create_order.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == create_order.id
        assert response.data['status'] == create_order.status

    def test_update_order_status_unauthenticated_return_401(self, api_client, create_order):
        """Test updating an order status."""
        data = {'status': Order.SERVED_DISH}
        response = api_client.patch(f'/api/orders/{create_order.id}/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_order_status_authenticated_return_403(self, authenticated_user, create_order):
        """Test updating an order status."""
        data = {'status': Order.SERVED_DISH}
        response = authenticated_user.patch(f'/api/orders/{create_order.id}/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_order_status_admin_return_200(self, admin_user, create_order):
        """Test updating an order status."""
        data = {'status': Order.SERVED_DISH}
        response = admin_user.patch(f'/api/orders/{create_order.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        create_order.refresh_from_db()
        assert create_order.status == Order.SERVED_DISH

    def test_delete_order_unauthenticated_return_401(self, api_client, create_order):
        """Test deleting an order."""
        response = api_client.delete(f'/api/orders/{create_order.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_order_authenticated_return_403(self, authenticated_user, create_order):
        """Test deleting an order."""
        response = authenticated_user.delete(f'/api/orders/{create_order.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_order_admin_return_204(self, admin_user, create_order):
        """Test deleting an order."""
        response = admin_user.delete(f'/api/orders/{create_order.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(id=create_order.id).exists()
