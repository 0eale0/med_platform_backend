from django.db import models


class Menu(models.Model):
    pass


class Day(models.Model):
    done = models.BooleanField(default=False, blank=True)
    number = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)


class Dish(models.Model):
    user = models.ForeignKey("accounts.User", on_delete = models.SET_NULL, null=True)
    is_for_all = models.BooleanField(default=False)

    name = models.CharField(max_length=60)
    default_weight = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()
    recipe = models.TextField()

    day = models.ManyToManyField(Day, through="DayDish")


class DayDish(models.Model):
    dish_amount = models.FloatField()
    time = models.TimeField()
    comment = models.CharField(max_length=255, null=True, blank=True)

    additional_to = models.ForeignKey('DayDish', default=None, on_delete=models.CASCADE, blank=True, null=True)

    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=60)
    default_weight = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()

    dish = models.ManyToManyField(Dish, through="DishIngredient")


class DishIngredient(models.Model):
    ingredient_amount = models.FloatField()

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # без паники, тут нет лишних запросов, но лучше проверьте
    @property
    def get_ingredient_name(self):
        return self.ingredient.name

    @property
    def get_ingredient_id(self):
        return self.ingredient.name

    @property
    def get_ingredient_default_weight(self):
        return self.ingredient.default_weight
