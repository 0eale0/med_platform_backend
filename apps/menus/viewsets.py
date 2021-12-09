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
        day_dishes = request.data["dishes"]

        for day_dish in day_dishes:
            dish = Dish.objects.filter(id=day_dish["id"]).first()
            DayDish.objects.create(
                time=day_dish["time"],
                dish_amount=day_dish["amount"],
                day=day,
                dish=dish,
            )

        return Response(serializers.DaySerializer(day).data)

    def retrieve(self, request, *args, **kwargs):
        day = self.get_object()
        day_dishes = DayDish.objects.filter(day_id=day.id).all()
        dishes = []

        for day_dish in day_dishes:
            serializer = serializers.DayDishSerializer(day_dish).data
            dish = dict(
                **serializer["dish"],
                time=serializer["time"],
                amount=serializer["dish_amount"]
            )
            del dish["day"]
            dishes.append(dish)

        serializer_day = {**self.get_serializer(day).data, "dishes": dishes}
        del serializer_day["menu"]

        return Response(serializer_day)


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    def create(self, request, *args, **kwargs):
        dish = Dish.objects.create(**request.data["dish"])
        ingredients = request.data["ingredients"]

        for ingredient in ingredients:
            class_ingredient = Ingredient.objects.filter(id=ingredient["id"]).first()
            DishIngredient.objects.create(
                ingredient_amount=ingredient["amount"],
                dish=dish,
                ingredient=class_ingredient,
            )
        return Response(serializers.DishSerializer(dish).data)

    def retrieve(self, request, *args, **kwargs):
        dish = self.get_object()
        dish_ingredients = DishIngredient.objects.filter(dish_id=dish.id).all()
        ingredients = []

        for dish_ingredient in dish_ingredients:
            serializer = serializers.DishIngredientSerializer(dish_ingredient).data
            ingredient = dict(
                **serializer["ingredient"], amount=serializer["ingredient_amount"]
            )
            del ingredient["dish"]
            ingredients.append(ingredient)

        serializer_dish = {**self.get_serializer(dish).data, "ingredients": ingredients}
        del serializer_dish["day"]

        return Response(serializer_dish)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()
