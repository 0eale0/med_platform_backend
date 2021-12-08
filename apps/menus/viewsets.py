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
        day = request.data['day']
        day = Dish(**day)
        day_dishes = request.data['day_dishes']
        classes = []

        for day_dish in day_dishes:
            classes.append(DayDish(**day_dish, dish_id=day.id))

        request.data = request.data['day']
        response = super().create(request, *args, **kwargs)
        return response
    
    def retrieve(self, request, *args, **kwargs):
        day = self.get_object()
        if not request.user.post:
            return Response({'detail': 'У вас недостаточно прав для выполнения данного действия.'}, status=401)
        return Response(self.get_serializer(day).data)


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    def create(self, request, *args, **kwargs):
        dish = request.data['dish']
        dish = Dish(**dish)
        dish_ingredients = request.data['dish_ingredients']

        for dish_ingredient in dish_ingredients:
            DishIngredient(**dish_ingredient, dish_id=dish.id)

        request.data = request.data['dish']
        response = super().create(request, *args, **kwargs)
        return response

    def retrieve(self, request, *args, **kwargs):
        dish = self.get_object()
        if not request.user.post:
            return Response({'detail': 'У вас недостаточно прав для выполнения данного действия.'}, status=401)
        return Response(self.get_serializer(dish).data)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()
