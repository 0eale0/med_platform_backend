from django.shortcuts import render
from rest_framework import viewsets

from apps.menus import models, serializers


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MenuSerializer
    queryset = models.Menu.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()
