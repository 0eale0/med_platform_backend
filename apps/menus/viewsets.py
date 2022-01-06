import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import Patient
from apps.menus import serializers
from apps.menus.models import Menu, Ingredient, Day, Dish, DayDish, DishIngredient
from apps.menus.permissions import IsDoctor, IsOwnerOrReadOnlyDay
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
    permission_classes = [IsAuthenticated & IsDoctor]

    @action(methods=['GET'], detail=True)
    def day_list(self, request, pk=None):
        patient = Patient.objects.filter(id=pk).first()
        days = Day.objects.filter(menu=patient.menu).all()
        days_serialized = []
        for day in days:
            day_serialized = DaySerializer(day).data
            days_serialized.append(day_serialized)
        return Response(days_serialized)


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated & IsDoctor]


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnlyDay]

    def create(self, request, *args, **kwargs):
        menu = Menu.objects.filter(id=request.data["menu_id"]).first()
        day = Day.objects.create(menu=menu, done=False, number=request.data["day_number"])
        day_dishes = request.data["dishes"]

        for day_dish in day_dishes:
            dish = Dish.objects.filter(id=day_dish["id"]).first()
            DayDish.objects.create(
                time=day_dish["time"],
                dish_amount=day_dish["amount"],
                day=day,
                dish=dish,
            )

        serializer = serializers.DaySerializer(day)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        day = self.get_object()
        day_dishes = DayDish.objects.filter(day_id=day.id).all()
        dishes = []

        for day_dish in day_dishes:
            day_dish_serializer = serializers.DayDishSerializer(day_dish).data
            dish = dict(
                **day_dish_serializer["dish"],
                time=day_dish_serializer["time"],
                amount=day_dish_serializer["dish_amount"]
            )
            del dish["day"]
            dishes.append(dish)

        day_serializer = {**self.get_serializer(day).data, "dishes": dishes}
        del day_serializer["menu"]

        return Response(day_serializer)

    @action(methods=['POST'], detail=False)
    def create_day(self, request):
        patient = Patient.objects.filter(id=request.data["patient_id"]).first()
        last_day = Day.objects.filter(menu=patient.menu).order_by('-number').first()
        day_number = last_day.number + 1 if last_day else 1
        new_day = Day.objects.create(number=day_number, menu=patient.menu)
        new_day.save()
        return Response(DaySerializer(new_day).data)

    @action(methods=['POST'], detail=False)
    def get_day(self, request):
        if "patient_id" in request.data.keys():
            patient = Patient.objects.filter(id=request.data["patient_id"]).first()
        else:
            patient = Patient.objects.filter(user=request.user).first()
        day = Day.objects.filter(number=request.data["day_number"], menu=patient.menu).first()
        return Response(DaySerializer(day).data)


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    permission_classes = [IsAuthenticated & IsDoctor]

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

        serializer = serializers.DishSerializer(dish)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        dish = self.get_object()
        dish_ingredients = DishIngredient.objects.filter(dish_id=dish.id).all()
        ingredients = []

        for dish_ingredient in dish_ingredients:
            dish_ingredient_serializer = serializers.DishIngredientSerializer(dish_ingredient).data
            ingredient = dict(
                **dish_ingredient_serializer["ingredient"], amount=dish_ingredient_serializer["ingredient_amount"]
            )
            del ingredient["dish"]
            ingredients.append(ingredient)

        dish_serializer = {**self.get_serializer(dish).data, "ingredients": ingredients}
        del dish_serializer["day"]

        return Response(dish_serializer)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()
    permission_classes = [IsAuthenticated]  # TODO: Set IsDoctor or IsDayOwner

    def create(self, request, *args, **kwargs):
        hours, minutes, *_ = list(map(int, request.data["time"].split(":")))
        day_dish = DayDish.objects.create(
            dish_amount=request.data["dish_amount"],
            time=datetime.time(hour=hours, minute=minutes),
            day=Day.objects.filter(id=int(request.data["day_id"])).first(),
            dish=Dish.objects.filter(id=int(request.data["dish_id"])).first(),
        )
        day_dish.save()
        day_dish_serializer = serializers.DayDishSerializer(day_dish).data
        result = dict(
            day_dish_serializer["dish"],
            amount=day_dish_serializer["dish_amount"],
            time=day_dish_serializer["time"],
            day_dish_id=day_dish_serializer["id"],
        )
        del result["day"]
        return Response(result)

    @action(methods=['POST'], detail=False)
    def day_dish_list(self, request):
        if "patient_id" in request.data.keys():
            patient = Patient.objects.filter(id=request.data["patient_id"]).first()
        else:
            patient = Patient.objects.filter(user=request.user).first()
        day = Day.objects.filter(number=request.data["day_number"], menu=patient.menu).first()
        day_dishes = DayDish.objects.filter(day_id=day.id)

        day_dishes_serialized = []
        for day_dish in day_dishes:
            day_dish_serializer = serializers.DayDishSerializer(day_dish).data
            result = dict(
                day_dish_serializer["dish"],
                amount=day_dish_serializer["dish_amount"],
                time=day_dish_serializer["time"],
                day_dish_id=day_dish_serializer["id"],
            )
            del result["day"]
            day_dishes_serialized.append(result)
        return Response(day_dishes_serialized)


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()
    permission_classes = [IsAuthenticated & IsDoctor]
