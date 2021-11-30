from django.contrib import admin

from apps.menus.models import Menu, Day, Ingredient, Dish, DishIngredient, DayDish

admin.site.register(Menu)
admin.site.register(Day)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(DishIngredient)
admin.site.register(DayDish)
