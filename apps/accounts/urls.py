from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import ActivateUserView
from apps.accounts.viewsets import PatientViewForDoctor

router = routers.SimpleRouter()

router.register("api/accounts/patient/?", PatientViewForDoctor)


urlpatterns = [
    path(r"api/auth/token/", TokenObtainPairView.as_view()),
    path(r"api/auth/token/refresh/", TokenRefreshView.as_view()),
    path(r"api/accounts/activate/", ActivateUserView.as_view()),
]
