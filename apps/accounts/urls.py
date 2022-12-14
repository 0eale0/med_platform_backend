from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import (
    ActivateUserView,
    WhoAmIView,
    VerifyEmailView,
    ObjectHistory,
    CalculateCPFC,
    GetDoctor,
    ResetPasswordView,
    SendEmailResetPasswordView,
)
from apps.accounts.viewsets import PatientViewForDoctor, DoctorViewSet

router = routers.SimpleRouter()

router.register("api/accounts/patient/?", PatientViewForDoctor)
router.register("api/accounts/doctor/?", DoctorViewSet)

urlpatterns = [
    path(r"api/auth/token/", TokenObtainPairView.as_view()),
    path(r"api/auth/token/refresh/", TokenRefreshView.as_view()),
    path(r"api/accounts/activate/", ActivateUserView.as_view(), name="ActivateUser"),
    path(r"api/accounts/whoami/", WhoAmIView.as_view()),
    path(r"api/accounts/VerifyEmail/<token>/", VerifyEmailView.as_view(), name="VerifyEmail"),
    path(r"api/accounts/history/<model>/<pk>/", ObjectHistory.as_view()),
    path(r"api/accounts/calculatecpfc/<pk>/", CalculateCPFC.as_view()),
    path(r"api/accounts/get_doctor/", GetDoctor.as_view()),
    path(r"api/accounts/ResetPassword/<token>/", ResetPasswordView.as_view(), name="ResetPassword"),
    path(r"api/accounts/SendEmailResetPassword/", SendEmailResetPasswordView.as_view()),
]
