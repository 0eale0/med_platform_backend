import pytest

from rest_framework.test import APITestCase, APIClient
from tests.test_accounts.factories import UserFactory, DoctorFactory, PatientFactory
from tests.test_menus.factories import MenuFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class InitUsers(APITestCase):
    def init_menu(self):
        self.menu_1 = MenuFactory()
        self.menu_2 = MenuFactory()

    def init_doctor(self) -> None:
        self.user_doctor = UserFactory(email='doc@mail.ru')
        self.doctor = DoctorFactory(user=self.user_doctor)

    def auth_doctor(self) -> None:
        self.doctor_authorized = APIClient()
        response_for_doctor = self.doctor_authorized.post("/api/auth/token/",
                                                          {'email': 'doc@mail.ru', 'password': '123'})

        self.access_token = response_for_doctor.json()['access']
        self.doctor_authorized.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def init_patients(self) -> None:
        self.user_patient1 = UserFactory(email='patient@mail.ru')
        self.user_patient2 = UserFactory()
        self.patient1 = PatientFactory(user=self.user_patient1, doctor=self.doctor, menu_id=self.menu_1.id)
        self.patient2 = PatientFactory(user=self.user_patient2, doctor=self.doctor, menu_id=self.menu_2.id)

    def auth_patient(self) -> None:
        self.patient_authorized = APIClient()
        response_for_patient = self.patient_authorized.post("/api/auth/token/",
                                                            {'email': 'patient@mail.ru', 'password': '123'})
        self.access_token = response_for_patient.json()['access']
        self.patient_authorized.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def setUp(self) -> None:
        self.init_doctor()
        self.auth_doctor()

        self.init_menu()

        self.init_patients()
        self.auth_patient()
