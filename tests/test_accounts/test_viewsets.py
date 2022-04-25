from tests.conftest import InitUsers


class TestPatientViewForDoctor(InitUsers):
    def test_get_list_patient(self):
        url = '/api/accounts/patient/'
        response = self.doctor_authorized.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    # fix backend and uncomment this test
    # def test_get_info_about_patient(self):
    #     url = '/api/accounts/patient/1/'
    #     response = self.doctor_authorized.get(url, {"patient_id": self.patient1.id})
    #     assert response.status_code == 200
    #     assert response.json()["id"] == self.patient1.id
