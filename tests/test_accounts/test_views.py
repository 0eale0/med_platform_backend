from tests.conftest import InitUsers


class TestWhoAmI(InitUsers):
    def test_doctor_response(self):
        url = '/api/accounts/whoami/'
        response = self.doctor_authorized.get(url)

        values_to_check = ("first_name", "last_name", "middle_name", "email")
        constants = {"is_doctor": True, "is_patient": False}

        info_from_object = {**{value: getattr(self.doctor.user, value) for value in values_to_check}, **constants}
        info_from_response = {
            **{value: response.json()[value] for value in values_to_check},
            **{value: response.json()[value] for value in constants.keys()},
        }

        assert response.status_code == 200
        assert info_from_object == info_from_response

    def test_patient_response(self):
        url = '/api/accounts/whoami/'
        response = self.patient_authorized.get(url)

        values_to_check = ("first_name", "last_name", "middle_name", "email")
        constants = {"is_doctor": False, "is_patient": True}

        info_from_object = {**{value: getattr(self.patient1.user, value) for value in values_to_check}, **constants}
        info_from_response = {
            **{value: response.json()[value] for value in values_to_check},
            **{value: response.json()[value] for value in constants.keys()},
        }

        assert response.status_code == 200
        assert info_from_object == info_from_response

    def test_anonymous_response(self):
        url = '/api/accounts/whoami/'
        response = self.anonymous_user.get(url)

        response_result = response.json()
        await_result = {'error': 'Войдите в аккаунт, чтобы увидеть информацию'}

        assert response_result == await_result
