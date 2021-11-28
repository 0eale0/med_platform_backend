from django.contrib import admin

from apps.accounts.models import User, Patient, Doctor, DoctorPatient

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(DoctorPatient)

