from rest_framework import routers

from apps.menus.viewsets import (
    MenuViewSet,
    IngredientViewSet,
    DayViewSet,
    DishViewSet,
    DayDishViewSet,
    DishIngredientViewSet,
    DishForPatient,
    NewDayViewSet,
)

router = routers.SimpleRouter()

router.register("api/menus/menus/?", MenuViewSet)
router.register("api/menus/new_day/?", NewDayViewSet)
router.register("api/menus/ingredients/?", IngredientViewSet)
router.register("api/menus/day/?", DayViewSet)
router.register("api/menus/dish/?", DishViewSet)
router.register("api/menus/day_dish/?", DayDishViewSet)
router.register("api/menus/dish_ingredients/?", DishIngredientViewSet)
router.register("api/menus/dish_patient/?", DishForPatient)
