import json
import pytest

# from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django_mock_queries.mocks import MockSet

from apps.accounts.viewsets import PatientViewForDoctor
from tests.test_accounts.factories import UserFactory, DoctorFactory, PatientFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestPatientViewForDoctor(APITestCase):
    def setUp(self):
        user_doctor = UserFactory(email='doc@mail.ru')
        user_patient1, user_patient2 = UserFactory(), UserFactory()

        self.doctor = DoctorFactory(user=user_doctor)
        self.patient1 = PatientFactory(user=user_patient1)
        self.patient2 = PatientFactory(user=user_patient2)

        self.client = APIClient()
        response = self.client.post("/api/auth/token/", {'email': 'doc@mail.ru', 'password': '123'})
        # assert response.json() == 0
        self.access_token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_get_list_patient(self, mocker, rf):
        url = '/api/accounts/patient/'
        request = self.client.get(url)
        qs = MockSet(
            self.patient1,
            self.patient2
        )
        view = PatientViewForDoctor.as_view(
            {'get': 'list'}
        )
        mocker.patch.object(PatientViewForDoctor, 'get_queryset', return_value=qs)
        response = view(request).render()
        assert response == 200
        assert len(json.loads(response.content)) == 2
