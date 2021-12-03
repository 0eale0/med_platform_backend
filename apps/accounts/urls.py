from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('patient/', views.patient_list),
    path('patient/<int:pk>/', views.patient_detail),
]