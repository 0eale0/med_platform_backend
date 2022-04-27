from tests.conftest import InitUsers


class TestPatientViewForDoctor(InitUsers):
    def test_get_list_patient(self):
        url = '/api/accounts/patient/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_info_about_patient(self):
        url = f'/api/accounts/patient/{self.patient1.id}/'
        response = self.doctor_authorized.get(url, {"patient_id": self.patient1.id})
        assert response.status_code == 200
        assert response.json()["id"] == self.patient1.id
