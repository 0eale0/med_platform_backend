from rest_framework import routers
from apps.accounts.viewsets import PatientViewForDoctor

router = routers.SimpleRouter()

router.register('api/accounts/patient/?', PatientViewForDoctor)
