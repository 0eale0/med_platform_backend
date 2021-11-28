from django.db import models

from apps.accounts.models import Patient


class Menu(models.Model):
    pass


class PatientMenu(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class Day(models.Model):
    done = models.BooleanField(default=False, blank=True)
    number = models.IntegerField()


class MenuDay(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=60)
    default_weight = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()


class Dish(models.Model):
    name = models.CharField(max_length=60)
    default_weight = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()
    recipe = models.TextField()


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredient_amount = models.FloatField()


class DayDish(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    dish_amount = models.FloatField()
    time = models.TimeField()
