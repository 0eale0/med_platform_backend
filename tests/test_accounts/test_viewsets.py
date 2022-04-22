from django.test import TestCase

from apps.accounts.viewsets import PatientViewForDoctor


class ExampleTest(TestCase):
    def test_te(self):
        pass


class PatientViewForDoctorTest(TestCase):
    def test_get_list_patient(self):
        viewset = PatientViewForDoctor.as_view({'get': 'list'})
