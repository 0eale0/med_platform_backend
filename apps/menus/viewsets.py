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
        day = Day.objects.create(**request.data["day"])
        dish_ingredients = request.data["day_dishes"]

        for day_dish in dish_ingredients:
            class_day = Day.objects.filter(id=day.id).first()
            class_dish = Ingredient.objects.filter(id=day_dish["id_dish"]).first()
            DishIngredient.objects.create(
                ingredient_amount=day_dish["ingredient_amount"],
                day=class_day,
                dish=class_dish,
            )

        serializer = self.get_serializer(data=request.data["day"])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        day = self.get_object()
        if not request.user.post:
            return Response(
                {"detail": "У вас недостаточно прав для выполнения данного действия."},
                status=401,
            )
        return Response(self.get_serializer(day).data)


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    def create(self, request, *args, **kwargs):
        dish = Dish.objects.create(**request.data["dish"])
        dish_ingredients = request.data["dish_ingredients"]

        for dish_ingredient in dish_ingredients:
            class_dish = Dish.objects.filter(id=dish.id).first()
            class_ingredient = Ingredient.objects.filter(
                id=dish_ingredient["id_ingredient"]
            ).first()
            DishIngredient.objects.create(
                ingredient_amount=dish_ingredient["ingredient_amount"],
                dish=class_dish,
                ingredient=class_ingredient,
            )

        serializer = self.get_serializer(data=request.data["dish"])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        dish = self.get_object()
        if not request.user.post:
            return Response(
                {"detail": "У вас недостаточно прав для выполнения данного действия."},
                status=401,
            )
        return Response(self.get_serializer(dish).data)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()
