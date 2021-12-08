import dish as dish
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.menus import serializers
from apps.menus.models import Menu, Ingredient, Day, Dish, DayDish, DishIngredient
from apps.menus.serializers import (
    MenuSerializer,
    IngredientSerializer,
    DaySerializer,
    DishSerializer,
    DayDishSerializer,
    DishIngredientSerializer,
)


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()

    def create(self, request, *args, **kwargs):
        menu = Menu.objects.filter(id=request.data["menu_id"]).first()
        day = Day.objects.create(menu=menu, **request.data["day"])
        day_dishes = request.data["day_dishes"]
        list_day_dishes = []

        for day_dish in day_dishes:
            dish = Dish.objects.filter(id=day_dish["id_dish"]).first()
            DayDish.objects.create(
                time=day_dish["time"],
                dish_amount=day_dish["amount"],
                day=day,
                dish=dish,
            )

            copy_dict = dish.__dict__.copy()
            copy_dict.pop("_state")
            copy_dict.update(amount=day_dish["amount"])
            list_day_dishes.append(copy_dict)

        day_dict = day.__dict__.copy()
        day_dict.pop("_state")
        day_dict.update({**request.data["day"], "day_dishes": list_day_dishes})

        return Response(day_dict, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        day = self.get_object()
        list_day_dishes = []
        day_dishes = DayDish.objects.filter(day_id=day.id).all()

        for day_dish in day_dishes:
            copy_dict = day_dish.__dict__.copy()
            copy_dict.pop("_state")
            list_day_dishes.append(copy_dict)

        day_dict = day.__dict__.copy()
        day_dict.pop("_state")
        day_dict.update({"day_dishes": list_day_dishes})

        return Response(day_dict, status=status.HTTP_201_CREATED)


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    def create(self, request, *args, **kwargs):
        dish = Dish.objects.create(**request.data["dish"])
        ingredients = request.data["ingredients"]
        list_ingredients = []

        for ingredient in ingredients:
            class_ingredient = Ingredient.objects.filter(id=ingredient["id"]).first()
            DishIngredient.objects.create(
                ingredient_amount=ingredient["amount"],
                dish=dish,
                ingredient=class_ingredient,
            )

            copy_dict = class_ingredient.__dict__.copy()
            copy_dict.pop("_state")
            copy_dict.update(amount=ingredient["amount"])
            list_ingredients.append(copy_dict)

        dish_dict = dish.__dict__.copy()
        dish_dict.pop("_state")
        dish_dict.update({"ingredients": list_ingredients})

        return Response(dish_dict, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        dish = self.get_object()
        list_ingredients = []
        ingredients = DishIngredient.objects.filter(dish_id=dish.id).all()

        for ingredient in ingredients:
            copy_dict = ingredient.__dict__.copy()
            copy_dict.pop("_state")
            list_ingredients.append(copy_dict)

        dish_dict = dish.__dict__.copy()
        dish_dict.pop("_state")
        dish_dict.update({"ingredients": list_ingredients})

        return Response(dish_dict, status=status.HTTP_201_CREATED)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()
