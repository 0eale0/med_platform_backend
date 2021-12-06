from django.shortcuts import render
from rest_framework import viewsets

from apps.menus.models import Menu, Ingredient, Day, Dish, DayDish, DishIngredient
from apps.menus.serializers import MenuSerializer, IngredientSerializer, DaySerializer, DishSerializer, \
    DayDishSerializer, DishIngredientSerializer


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()

