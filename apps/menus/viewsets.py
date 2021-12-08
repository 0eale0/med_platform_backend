from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

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


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)  # ingredients_id
        request.data = data["ingredients_id"]

        dish_ingredients = DishIngredientViewSet()
        dish_ingredients.create(request)
        del data["ingredients_id"]

        request.data = bytes(data)
        response = super().create(request, *args, **kwargs)
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            for data in request.data:
                serializer = self.get_serializer(data=bytes(data))
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

            return Response({"error": False, "status": 200})
        else:
            response = super().create(request, *args, **kwargs)
            return response

