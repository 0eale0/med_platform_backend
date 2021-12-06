from rest_framework import serializers

from apps.menus.models import Menu, Ingredient, Dish, Day, DayDish, DishIngredient


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    menu = MenuSerializer()

    class Meta:
        model = Day
        fields = '__all__'


class DayDishSerializer(serializers.ModelSerializer):
    day = DaySerializer()
    dish = DishSerializer()

    class Meta:
        model = DayDish
        fields = '__all__'


class DishIngredientSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    ingredient = IngredientSerializer()

    class Meta:
        model = DishIngredient
        fields = '__all__'
