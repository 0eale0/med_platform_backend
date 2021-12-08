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
        day_dishes = request.data["day_dishes"]

        for day_dish in day_dishes:
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
        ingredients = request.data["ingredients"]
        list_ingredients = []

        for ingredient in ingredients:
            class_ingredient = Ingredient.objects.filter(
                id=ingredient["id"]
            ).first()
            DishIngredient.objects.create(
                ingredient_amount=ingredient["amount"],
                dish=dish,
                ingredient=class_ingredient,
            )

            copy_dict = class_ingredient.__dict__.copy()
            copy_dict.pop("_state")
            copy_dict.update(amount=ingredient["amount"])
            list_ingredients.append(copy_dict)

        dish_dict = {"id": dish.id}
        dish_dict.update({**request.data["dish"], "ingredients": list_ingredients})

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
