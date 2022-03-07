from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import ActivateUserView, WhoAmIView, VerifyEmailView
from apps.accounts.viewsets import PatientViewForDoctor

router = routers.SimpleRouter()

router.register("api/accounts/patient/?", PatientViewForDoctor)


urlpatterns = [
    path(r"api/auth/token/", TokenObtainPairView.as_view()),
    path(r"api/auth/token/refresh/", TokenRefreshView.as_view()),
    path(r"api/accounts/activate/", ActivateUserView.as_view()),
    path(r"api/accounts/whoami/", WhoAmIView.as_view()),
    path(r"api/accounts/VerifyEmail/<uid_64>/<token>/", VerifyEmailView.as_view(), name="VerifyEmail")
]
