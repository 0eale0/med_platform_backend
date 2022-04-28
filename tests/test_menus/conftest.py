from tests.conftest import InitUsers
from tests.test_menus.factories import DayFactory, DishFactory, DayDishFactory, IngredientFactory, DishIngredientFactory


class InitMenu(InitUsers):
    def init_day(self):
        self.day = DayFactory(menu=self.menu_1)

    def init_dish(self):
        self.dish_1 = DishFactory()
        self.dish_2 = DishFactory()

    def init_day_dish(self):
        self.day_dish_1 = DayDishFactory(day=self.day, dish=self.dish_1)
        self.day_dish_2 = DayDishFactory(day=self.day, dish=self.dish_2)

    def init_ingredient(self):
        self.ingredient_1 = IngredientFactory(name="potato")
        self.ingredient_2 = IngredientFactory(name="oil")

    def init_dish_ingredient(self):
        self.dish_ingredient_1 = DishIngredientFactory(dish=self.dish_1, ingredient=self.ingredient_1)
        self.dish_ingredient_2 = DishIngredientFactory(dish=self.dish_2, ingredient=self.ingredient_2)

    def setUp(self):
        super().setUp()

        self.init_menu()
        self.init_day()
        self.init_dish()
        self.init_day_dish()
        self.init_ingredient()
        self.init_dish_ingredient()
