import json

import pytest
from django.urls import reverse
from django_mock_queries.mocks import MockSet
from apps.accounts.viewsets import PatientViewForDoctor
from tests.test_accounts.factories import patient1

# pytestmark = [pytest.mark.urls('config.urls'), pytest.mark.unit]


class TestPatientViewForDoctor:
    def test_get_list_patient(self, mocker, rf):
        pass
        # url = reverse('currency-list')
        # request = rf.get(url)
        # qs = MockSet(
        #     patient1
        # )
        # view = PatientViewForDoctor.as_view(
        #     {'get': 'list'}
        # )
        # mocker.patch.object(PatientViewForDoctor, 'get_queryset', return_value=qs)
        # response = view(request).render()
        # assert response.status_code == 200
        # assert len(json.loads(response.content)) == 3
