from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.menus.models import Menu
from apps.accounts.auth import UserProfileManager

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)

    middle_name = models.CharField(max_length=150, **NULLABLE)
    first_name = models.CharField(_("first name"), max_length=150, **NULLABLE)
    last_name = models.CharField(_("last name"), max_length=150, **NULLABLE)

    objects = UserProfileManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.username}'


class Doctor(models.Model):
    phone_number = models.CharField(max_length=100)
    post = models.CharField(max_length=100)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Patient(models.Model):
    phone_number = models.CharField(max_length=100, **NULLABLE)  # unique=True
    medical_card_number = models.CharField(max_length=255, **NULLABLE)
    insurance_policy_number = models.CharField(max_length=100, **NULLABLE)
    birth_date = models.DateField(**NULLABLE)
    link_token = models.CharField(max_length=100, **NULLABLE)
    sex = models.CharField(max_length=6, choices=[("male", "male"), ("female", "female")], **NULLABLE)
    activity_level = models.CharField(max_length=255, **NULLABLE)
    weight = models.FloatField(**NULLABLE)
    waist = models.FloatField(**NULLABLE)
    height = models.FloatField(**NULLABLE)
    hips = models.IntegerField(**NULLABLE)
    medical_information = models.TextField(**NULLABLE)
    country = models.CharField(max_length=60, **NULLABLE)
    city = models.CharField(max_length=60, **NULLABLE)
    address = models.CharField(max_length=60, **NULLABLE)

    user = models.OneToOneField(User, on_delete=models.CASCADE, **NULLABLE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, **NULLABLE)  # почему пациент не может существовать без доктора?
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, **NULLABLE)  # лишнее поле

    def __str__(self):
        return f"{self.user.username}"
