from model_bakery import baker

from apps.accounts.models import User, Doctor, Patient

user_doctor, user_patient1, user_patient2 = baker.make(User, _quantity=3)

baker.make(Doctor, user=user_doctor)
baker.make(Patient, user=user_patient1)
baker.make(Patient, user=user_patient2)
