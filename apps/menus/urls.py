from rest_framework import routers
from django.urls import path, include

from apps.menus import views

router = routers.DefaultRouter()
router.register('menus', views.MenuViewSet)
router.register('ingredients', views.IngredientViewSet)

urlpatterns = [
    path(r'api/', include(router.urls))
]
