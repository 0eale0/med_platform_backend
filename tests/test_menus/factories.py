import datetime

import factory

from apps.menus.models import Dish, Day, Menu, DayDish, Ingredient, DishIngredient


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu


class DayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Day

    done = False
    number = 1

    menu = factory.SubFactory(MenuFactory)


class DishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dish

    name = factory.Faker("name")
    default_weight = 100
    proteins = 10
    fats = 10
    carbohydrates = 10.1
    calories = 12.54
    recipe = "just do it"


class DayDishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DayDish

    dish_amount = 123
    comment = 'it is a comment'
    time = datetime.time(11)

    day = factory.SubFactory(DayFactory)
    dish = factory.SubFactory(DishFactory)


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Faker("name")
    default_weight = 12
    proteins = 12
    fats = 12
    carbohydrates = 12
    calories = 12


class DishIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DishIngredient

    ingredient_amount = 123

    dish = factory.SubFactory(DishFactory)
    ingredient = factory.SubFactory(IngredientFactory)
