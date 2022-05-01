import json

from tests.test_menus.conftest import InitMenu
from apps.menus.models import Day, Ingredient, Dish


class TestDishViewSet(InitMenu):
    def test_get_list_dishes(self):
        url = '/api/menus/dish/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['recipe'] == "just do it"

    def test_get_info_about_dish(self):
        url = f'/api/menus/dish/{self.dish_1.id}/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert response.json()['recipe'] == "just do it"

    def test_create(self):
        url = f"/api/menus/dish/"
        values_to_check = ["name", "default_weight", "proteins", "fats", "carbohydrates", "calories", "recipe"]

        data = {}
        dish_data = {value: getattr(self.dish_1, value) for value in values_to_check}

        data["dish"] = dish_data
        data["ingredients"] = [{"amount": 2, "id": self.ingredient_1.id}]

        response = self.doctor_authorized.post(url, data=data, format="json")
        object_from_db = Dish.objects.filter(id=response.json()["id"]).first()

        data_from_db = {value: getattr(object_from_db, value) for value in values_to_check}

        assert data_from_db == dish_data


class TestIngredientViewSet(InitMenu):
    def test_get_list_ingredients(self):
        url = '/api/menus/ingredients/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['name'] == "potato"

    def test_get_info_about_ingredient(self):
        url = f'/api/menus/ingredients/{self.ingredient_1.id}/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert response.json()['name'] == "potato"

    def test_create(self):
        url = f"/api/menus/ingredients/"
        values_to_check = ["name", "default_weight", "proteins", "fats", "carbohydrates", "calories"]

        data = {value: getattr(self.ingredient_1, value) for value in values_to_check}

        response = self.doctor_authorized.post(url, data=data)
        object_from_db = Ingredient.objects.filter(id=response.json()["id"]).first()

        data_from_db = {value: getattr(object_from_db, value) for value in data}

        assert data_from_db == data


class TestDayViewSet(InitMenu):
    def test_get_list_day(self):
        url = '/api/menus/day/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['number'] == 1

    def test_get_info_day(self):
        url = f'/api/menus/day/{self.day.id}/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert response.json()['number'] == 1
        assert response.json()['dishes'][0]['recipe'] == "just do it"

    def test_create(self):
        url = f"/api/menus/day/create_day/"
        response = self.doctor_authorized.post(url, data={"patient_id": self.patient1.id})

        day = Day.objects.filter(id=response.json()["id"]).first()

        assert day
