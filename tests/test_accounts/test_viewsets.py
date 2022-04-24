import pytest

from rest_framework.test import APITestCase, APIClient
from tests.test_accounts.factories import UserFactory, DoctorFactory, PatientFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class InitUsers(APITestCase):
    def setUp(self):
        self.user_doctor = UserFactory(email='doc@mail.ru')
        self.doctor = DoctorFactory(user=self.user_doctor)

        self.user_patient1, self.user_patient2 = UserFactory(email='patient@mail.ru'), UserFactory()
        self.patient1 = PatientFactory(user=self.user_patient1, doctor=self.doctor)
        self.patient2 = PatientFactory(user=self.user_patient2, doctor=self.doctor)

        self.doctor_authorized = APIClient()
        self.patient_authorized = APIClient()
        response_for_doctor = self.doctor_authorized.post("/api/auth/token/",
                                                          {'email': 'doc@mail.ru', 'password': '123'})
        response_for_patient = self.patient_authorized.post("/api/auth/token/",
                                                            {'email': 'patient@mail.ru', 'password': '123'})

        self.access_token = response_for_doctor.json()['access']
        self.doctor_authorized.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.access_token = response_for_patient.json()['access']
        self.patient_authorized.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)


class TestPatientViewForDoctor(InitUsers):
    def test_get_list_patient(self):
        url = '/api/accounts/patient/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_info_about_patient(self):
        url = '/api/accounts/patient/1/'
        response = self.doctor_authorized.get(url, {"patient_id": self.patient1.id})
        assert response.status_code == 200
        assert response.json()["id"] == self.patient1.id


class TestDishViewSet(InitUsers):
    pass
