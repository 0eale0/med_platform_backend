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
        await_result = {'error': 'login to view info'}

        assert response_result == await_result


class TestActivateUser(InitUsers):
    def test_user_activate(self):
        token = "token"

        patient = self.patient1
        patient.user_activate_token = token
        patient.user.is_active = False
        patient.user.save()
        patient.save()

        url = f'/api/accounts/activate/?token={token}'
        data = {"user": {"email": patient.user.email, "password": "123"}, "patient": {}}

        response = self.anonymous_user.post(url, data=data, format="json")
        assert response.status_code == 200

        patient.refresh_from_db()
        new_token = patient.user_activate_token

        url = f"/api/accounts/VerifyEmail/{new_token}/"

        response = self.anonymous_user.get(url)
        assert response.status_code == 200

        patient.refresh_from_db()

        assert patient.user.is_active == True


class TestResetPassword(InitUsers):
    def test_reset_password(self):
        patient = self.patient1
        start_password = patient.user.password

        url = f'/api/accounts/SendEmailResetPassword/'
        data = {"email": patient.user.email}
        response = self.anonymous_user.post(url, data=data, format="json")
        assert response.status_code == 200

        patient.refresh_from_db()
        password_reset_token = patient.password_reset_token

        url = f'/api/accounts/ResetPassword/{password_reset_token}/'
        data = {"password": "super_hard_password"}

        response = self.anonymous_user.post(url, data=data, format="json")
        assert response.status_code == 200

        patient.refresh_from_db()
        end_password = patient.user.password

        assert start_password != end_password
