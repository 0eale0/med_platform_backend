from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    middle_name = models.CharField(max_length=60)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    phone_number = models.CharField(max_length=100, null=False)
    medical_card_number = models.CharField(max_length=255)
    insurance_policy_number = models.CharField(max_length=100)
    birth_date = models.DateField(null=False)
    link_token = models.CharField(max_length=100, null=False)
    sex = forms.ChoiceField(choices=['male', 'female'])
    activity_level = models.CharField(max_length=255)
    weight = models.FloatField()
    waist = models.FloatField()
    height = models.FloatField()
    hips = models.IntegerField()
    medical_information = models.TextField()
    country = models.CharField(max_length=60, null=False)
    city = models.CharField(max_length=60, null=False)
    address = models.CharField(max_length=60, null=False)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    phone_number = models.CharField(max_length=100)
    post = models.CharField(max_length=100)


class DoctorPatient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


