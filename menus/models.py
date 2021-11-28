from django.db import models
from accounts.models import Patient


class Menu(models.Model):
    pass


class PatientMenu(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class Day(models.Model):
    done = models.BooleanField(null=False)
    number = models.IntegerField(null=False)


class MenuDay(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=60, null=False)
    default_weight = models.FloatField()
    proteins = models.FloatField(null=False)
    fats = models.FloatField(null=False)
    carbohydrates = models.FloatField(null=False)
    calories = models.FloatField(null=False)


class Dish(models.Model):
    name = models.CharField(max_length=60, null=False)
    default_weight = models.FloatField()
    proteins = models.FloatField(null=False)
    fats = models.FloatField(null=False)
    carbohydrates = models.FloatField(null=False)
    calories = models.FloatField(null=False)
    recipe = models.TextField()


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()


class DayDish(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    dish_amount = models.FloatField(null=False)
    time = models.TimeField(null=False)


