from tests.test_menus.conftest import InitMenu


class TestDishViewSet(InitMenu):
    def test_get_list_dishes(self):
        url = '/api/menus/dish/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['recipe'] == "just do it"

    def test_get_info_about_dish(self):
        url = '/api/menus/dish/1/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert response.json()['recipe'] == "just do it"


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
