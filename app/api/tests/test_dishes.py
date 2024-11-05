import pytest
from rest_framework import status
from model_bakery import baker
from api.models import Dish, Category
from core.models import User


@pytest.fixture
def create_category():
    """Fixture to create a Category instance."""
    return baker.make(Category)


@pytest.fixture
def create_dish(create_category):
    """Fixture to create a Dish associated with a category."""
    return baker.make(Dish, category=create_category)


@pytest.mark.django_db
class TestDishViewSet:

    def test_dish_list_unauthenticated_return_200(self, api_client):
        response = api_client.get("/api/dishes/")
        assert response.status_code == status.HTTP_200_OK

    def test_dish_list_authenticated_return_200(self, authenticated_user, create_dish):
        response = authenticated_user.get("/api/dishes/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == create_dish.name

    def test_create_dish_authenticated_return_201(self, admin_user, create_category):
        payload = {
            "name": "Pasta",
            "description": "Delicious pasta dish",
            "cost": "12.50",
            "available": True,
            "picture": "http://example.com/pasta.jpg",
            "category": create_category.id,
        }
        response = admin_user.post("/api/dishes/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Dish.objects.filter(name="Pasta").exists()

    def test_create_dish_unauthenticated_return_401(self, api_client, create_category):
        payload = {
            "name": "Pasta",
            "description": "Delicious pasta dish",
            "cost": "12.50",
            "available": True,
            "picture": "http://example.com/pasta.jpg",
            "category": create_category.id,
        }
        response = api_client.post("/api/dishes/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_dish_with_invalid_data_authenticated_return_400(self, admin_user):
        payload = {"name": "", "description": "No cost provided"}
        response = admin_user.post("/api/dishes/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "cost" in response.data

    def test_update_dish_authenticated_return_200(self, admin_user, create_dish):
        payload = {"name": "Updated Dish Name"}
        response = admin_user.patch(f"/api/dishes/{create_dish.id}/", payload)
        assert response.status_code == status.HTTP_200_OK
        create_dish.refresh_from_db()
        assert create_dish.name == "Updated Dish Name"

    def test_update_dish_unauthenticated_return_401(self, api_client, create_dish):
        payload = {"name": "Updated Dish Name"}
        response = api_client.patch(f"/api/dishes/{create_dish.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_dish_authenticated_return_204(self, admin_user, create_dish):
        response = admin_user.delete(f"/api/dishes/{create_dish.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Dish.objects.filter(id=create_dish.id).exists()

    def test_delete_dish_unauthenticated_return_401(self, api_client, create_dish):
        response = api_client.delete(f"/api/dishes/{create_dish.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_cannot_create_dish_return_403(self, authenticated_user, create_category):
        payload = {
            "name": "Non-Admin Dish",
            "description": "Non-admin user attempting to create a dish",
            "cost": "20.00",
            "available": True,
            "picture": "http://example.com/nonadmin.jpg",
            "category": create_category.id,
        }
        response = authenticated_user.post("/api/dishes/", payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN
