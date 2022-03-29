from django.db import models


class Menu(models.Model):  # Лишняя модель можно будет создать просто миграцией
    pass


class Day(models.Model):
    done = models.BooleanField(default=False, blank=True)
    number = models.IntegerField()

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class Dish(models.Model):
    name = models.CharField(max_length=60)
    default_weight = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()  # эти поля используются в нескольких моделях, можно вынести в абстрактную модель
    calories = models.FloatField()
    recipe = models.TextField()

    day = models.ManyToManyField(Day, through="DayDish")


class DayDish(models.Model):
    dish_amount = models.FloatField()
    time = models.TimeField()
    comment = models.CharField(max_length=255, null=True, blank=True)  # комментарии лучше текстфилд сделать

    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=60)
    default_weight = models.FloatField()
    proteins = models.FloatField()  # незаполнены параметры
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()

    dish = models.ManyToManyField(Dish, through="DishIngredient")


class DishIngredient(models.Model):
    ingredient_amount = models.FloatField()

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class AdditionalDayDish(models.Model):
    main_day_dish = models.ForeignKey(DayDish, on_delete=models.CASCADE, related_name='main_day_dish')
    additional_day_dish = models.ForeignKey(DayDish, on_delete=models.CASCADE, related_name='additional_day_dish')
