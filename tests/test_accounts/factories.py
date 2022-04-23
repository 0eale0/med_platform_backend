from model_bakery import baker

from apps.accounts.models import User, Doctor, Patient

user_doctor, user_patient1, user_patient2 = baker.prepare(User, _quantity=3)

doctor = baker.prepare(Doctor, user=user_doctor)
patient1 = baker.prepare(Patient, user=user_patient1)
patient2 = baker.prepare(Patient, user=user_patient2)
