from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from models import Dish, Day
from serializers import DishSerializer, DaySerializer


def dish_list(request):
    if request.method == "GET":
        dish = Dish.objects.all()
        serializer = DishSerializer(dish, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = DishSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def day_list(request):
    if request.method == "GET":
        day = Day.objects.all()
        serializer = DaySerializer(day, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = DaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
