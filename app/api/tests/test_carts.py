import pytest
from rest_framework import status
from model_bakery import baker
from api.models import Cart

@pytest.fixture
def create_cart():
    """Fixture to create a Cart instance."""
    return baker.make(Cart)

@pytest.mark.django_db
class TestCartViewSet:
    """Test class for Cart model."""

    def test_get_cart_creates_if_not_exists(self, api_client):
        """Test that a cart is created on GET if it doesn't already exist."""
        response = api_client.get("/api/carts/")
        assert response.status_code == status.HTTP_200_OK
        assert Cart.objects.count() == 1  
        assert "session_id" in response.data[0]  
        assert response.data[0]["session_id"] is not None  

    def test_user_cannot_create_cart_directly(self, api_client):
        """Test that the user cannot create a cart directly (POST should fail)."""
        response = api_client.post("/api/carts/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED 

    def test_user_cannot_update_cart_directly(self, api_client, create_cart):
        """Test that the user cannot update the cart directly (PATCH should fail)."""
        response = api_client.patch(f"/api/carts/{create_cart.id}/", {"session_id": "new_session"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_user_cannot_delete_cart(self, api_client, create_cart):
        """Test that the user cannot delete the cart (DELETE should fail)."""
        response = api_client.delete(f"/api/carts/{create_cart.id}/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

