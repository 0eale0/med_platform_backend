import json
import pytest

# from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django_mock_queries.mocks import MockSet

from apps.accounts.viewsets import PatientViewForDoctor
from tests.test_accounts.factories import UserFactory, DoctorFactory, PatientFactory


user_doctor = UserFactory.build(email='doc@mail.ru')
user_patient1, user_patient2 = UserFactory.build_batch(2)

doctor = DoctorFactory.build(user=user_doctor)
patient1 = PatientFactory.build(user=user_patient1)
patient2 = PatientFactory.build(user=user_patient2)


class TestPatientViewForDoctor(APITestCase):
    def setUp(self):
        self.client = APIClient()
        response = self.client.post("/api/auth/token/", {'email': 'doc@mail.ru'})
        assert response == 0
        self.access_token = response.json()['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_get_list_patient(self, mocker, rf):
        url = '/api/accounts/patient/'
        request = rf.get(url)
        qs = MockSet(
            patient1,
            patient2
        )
        view = PatientViewForDoctor.as_view(
            {'get': 'list'}
        )
        mocker.patch.object(PatientViewForDoctor, 'get_queryset', return_value=qs)
        response = view(request).render()
        assert response == 200
        assert len(json.loads(response.content)) == 2
