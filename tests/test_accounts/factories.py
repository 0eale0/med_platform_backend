import datetime

import factory

from django.contrib.auth.hashers import make_password

from apps.accounts.models import User, Doctor, Patient
from tests.test_menus.factories import MenuFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")

    username = factory.Faker("name")
    middle_name = 'sten'
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    password = make_password('123')


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Doctor

    phone_number = 890
    post = "yes"
    user = factory.SubFactory(UserFactory)


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    menu_id = factory.SubFactory(MenuFactory)

    user = factory.SubFactory(UserFactory)
    doctor = factory.SubFactory(DoctorFactory)
