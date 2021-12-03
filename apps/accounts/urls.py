from django.urls import path, include
from rest_framework import routers

from apps.accounts import views

router = routers.DefaultRouter()
router.register('users', views.UserView)
router.register('patient', views.PatientView)


urlpatterns = [
    path('api/account/', include(router.urls))
]
