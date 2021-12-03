from apps.menus import models
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = (
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = (
            'name', 'default_weight', 'proteins', 'fats', 'carbohydrates', 'calories', 'dish'
        )
