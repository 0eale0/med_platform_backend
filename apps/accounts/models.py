from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    middle_name = models.CharField(max_length=60)


class Doctor(models.Model):
    phone_number = models.CharField(max_length=100)
    post = models.CharField(max_length=100)

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Patient(models.Model):
    phone_number = models.CharField(max_length=100)
    medical_card_number = models.CharField(max_length=255, **NULLABLE)
    insurance_policy_number = models.CharField(max_length=100, **NULLABLE)
    birth_date = models.DateField()
    link_token = models.CharField(max_length=100)
    sex = forms.ChoiceField(choices=['male', 'female'])
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
