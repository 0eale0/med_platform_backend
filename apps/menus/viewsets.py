import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Patient
from apps.menus import serializers
from apps.menus.models import Menu, Ingredient, Day, Dish, DayDish, DishIngredient
from apps.menus.permissions import IsDoctor, IsOwnerOrReadOnlyDay, IsDayOwner
from apps.menus.serializers import (
    MenuSerializer,
    IngredientSerializer,
    DaySerializer,
    DishSerializer,
    DayDishSerializer,
    DishIngredientSerializer,
    DishListSerializer,
    DishDetailSerializer,
    DayDishDetailSerializer,
)


def get_patient(request) -> Patient:
    if "patient_id" in request.data.keys():
        return get_object_or_404(Patient, id=request.data["patient_id"])
    return Patient.objects.filter(user=request.user).first()


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated & IsDoctor]

    @action(methods=['GET'], detail=True)
    def day_list_1(self, request, pk=None):  # для чего оно тут
        patient = Patient.objects.filter(id=pk).first()
        days = Day.objects.filter(menu=patient.menu).all()
        days_serialized = []
        for day in days:
            day_serialized = DaySerializer(day).data
            days_serialized.append(day_serialized)
        return Response(days_serialized)

    @action(methods=['GET'], detail=False)
    def day_list_2(self, request):  # для чего оно тут
        patient = Patient.objects.filter(user=request.user).first()
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

        DayDish.objects.bulk_create(
            [
                DayDish(
                    time=day_dish["time"],
                    dish_amount=day_dish["amount"],
                    day=day,
                    dish=Dish.objects.filter(id=day_dish["id"]).first(),
                )
                for day_dish in day_dishes
            ]
        )

        serializer = serializers.DaySerializer(day)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        return Response(DayDishDetailSerializer(self.get_object()).data)

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
        patient = get_patient(request)
        day = Day.objects.filter(number=request.data["day_number"], menu=patient.menu).first()
        return Response(DaySerializer(day).data)


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    permission_classes = [IsAuthenticated & IsDoctor]

    def create(self, request, *args, **kwargs):
        dish = Dish.objects.create(**request.data["dish"])
        ingredients = request.data["ingredients"]

        DishIngredient.objects.bulk_create(
            [
                DishIngredient(ingredient_amount=ingredient["amount"], dish=dish, ingredient_id=ingredient["id"])
                for ingredient in ingredients
            ]
        )

        serializer = serializers.DishSerializer(dish)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        return Response(DishDetailSerializer(self.get_object()).data)


class DayDishViewSet(viewsets.ModelViewSet):
    serializer_class = DayDishSerializer
    queryset = DayDish.objects.all()
    permission_classes = [IsDoctor | IsDayOwner]

    def create(self, request, *args, **kwargs):
        hours, minutes, *_ = list(map(int, request.data["time"].split(":")))
        day_dish = DayDish.objects.create(
            dish_amount=request.data["dish_amount"],
            additional_to_id=request.data.get("additional_to"),
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
        patient = get_patient(request)

        day = Day.objects.filter(number=request.data["day_number"], menu=patient.menu).first()
        day_dishes = DayDish.objects.filter(day_id=day.id).all()
        return Response(DishListSerializer(day_dishes, many=True).data)

    @action(methods=['POST'], detail=False)
    def add_comment(self, request):
        comment = request.data["comment"]
        day_dish = DayDish.objects.filter(id=request.data["day_dish_id"]).first()

        day_dish.comment = comment
        day_dish.save()

        return Response({"status": "ok"})


class DishIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = DishIngredientSerializer
    queryset = DishIngredient.objects.all()
    permission_classes = [IsAuthenticated & IsDoctor]
