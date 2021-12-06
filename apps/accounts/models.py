from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.menus.models import Menu

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    middle_name = models.CharField(max_length=150)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)


class Doctor(models.Model):
    phone_number = models.CharField(max_length=100)
    post = models.CharField(max_length=100)

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Patient(models.Model):
    phone_number = models.CharField(max_length=100)  # unique=True
    medical_card_number = models.CharField(max_length=255, **NULLABLE)
    insurance_policy_number = models.CharField(max_length=100, **NULLABLE)
    birth_date = models.DateField()
    link_token = models.CharField(max_length=100)
    sex = forms.ChoiceField(choices=["male", "female"])
    activity_level = models.CharField(max_length=255, **NULLABLE)
    weight = models.FloatField(**NULLABLE)
    waist = models.FloatField(**NULLABLE)
    height = models.FloatField(**NULLABLE)
    hips = models.IntegerField(**NULLABLE)
    medical_information = models.TextField(**NULLABLE)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=60)

    user = models.OneToOneField(User, on_delete=models.CASCADE, **NULLABLE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, **NULLABLE)
