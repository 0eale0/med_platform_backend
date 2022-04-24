import pytest

from rest_framework.test import APITestCase, APIClient
from tests.test_accounts.factories import UserFactory, DoctorFactory, PatientFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestPatientViewForDoctor(APITestCase):
    def setUp(self):
        user_doctor = UserFactory(email='doc@mail.ru')
        self.doctor = DoctorFactory(user=user_doctor)

        user_patient1, user_patient2 = UserFactory(), UserFactory()
        self.patient1 = PatientFactory(user=user_patient1, doctor=self.doctor)
        self.patient2 = PatientFactory(user=user_patient2, doctor=self.doctor)

        self.client = APIClient()
        response = self.client.post("/api/auth/token/", {'email': 'doc@mail.ru', 'password': '123'})

        self.access_token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_get_list_patient(self):
        url = '/api/accounts/patient/'
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_info_about_patient(self):
        url = '/api/accounts/patient/1/'
        response = self.client.get(url, {"patient_id": self.patient1.id})
        assert response.status_code == 200
        assert response.json()["id"] == self.patient1.id
