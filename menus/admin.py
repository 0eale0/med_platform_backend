from django.contrib import admin
from .models import *

admin.site.register(Menu)
admin.site.register(PatientMenu)
admin.site.register(Day)
admin.site.register(MenuDay)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(DishIngredient)
admin.site.register(DayDish)
