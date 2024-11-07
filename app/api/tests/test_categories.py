
from datetime import time
import pytest
from rest_framework import status
from model_bakery import baker
from django.utils import timezone
from api.models import Category
from core.models import User

@pytest.fixture
def create_category():
    """Fixture to create a category for the authenticated user."""
    return baker.make(Category, time_period=Category.BOTH)


@pytest.mark.django_db
class TestCategory:
    """Test class for Category model."""

    def test_category_list_unauthenticated_return_200(self, api_client):
        response = api_client.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK

    def test_category_list_authenticated_return_200(self, authenticated_user, create_category):
        response = authenticated_user.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == create_category.name

    def test_create_category_unauthenticated_return_403(self, api_client):
        payload = {"name": "Groceries", "time_period": Category.MORNING}
        response = api_client.post("/api/categories/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_category_authenticated_return_403(self, authenticated_user):
        payload = {"name": "Groceries", "time_period": Category.MORNING}
        response = authenticated_user.post("/api/categories/", payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_admin_return_201(self, admin_user):
        payload = {"name": "Groceries", "time_period": Category.MORNING}
        response = admin_user.post("/api/categories/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="Groceries").exists()

    def test_create_category_with_empty_name_admin_return_400(self, admin_user):
        payload = {"name": "", "time_period": Category.EVENING}
        response = admin_user.post("/api/categories/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_update_category_admin_return_200(self, admin_user, create_category):
        payload = {"name": "New Category Name"}
        response = admin_user.patch(f"/api/categories/{create_category.id}/", payload)
        assert response.status_code == status.HTTP_200_OK
        create_category.refresh_from_db()
        assert create_category.name == "New Category Name"

    def test_update_category_unauthenticated_return_401(self, api_client, create_category):
        payload = {"name": "New Category Name"}
        response = api_client.patch(f"/api/categories/{create_category.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_category_authenticated_return_401(self,authenticated_user, create_category):
        payload = {"name": "New Category Name"}
        response = authenticated_user.patch(f"/api/categories/{create_category.id}/", payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_admin_return_204(self, admin_user, create_category):
        response = admin_user.delete(f"/api/categories/{create_category.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=create_category.id).exists()

    def test_delete_category_unauthenticated_return_401(self, api_client, create_category):
        response = api_client.delete(f"/api/categories/{create_category.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_category_authenticated_return_401(self, authenticated_user, create_category):
        response = authenticated_user.delete(f"/api/categories/{create_category.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
