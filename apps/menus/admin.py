from django.contrib import admin

from apps.menus.models import Menu, Day, Ingredient, Dish, DishIngredient, DayDish

admin.site.register(Day)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(DishIngredient)
admin.site.register(DayDish)


class DayInline(admin.TabularInline):
    model = Day
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [DayInline, ]
