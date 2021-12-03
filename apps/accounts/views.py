from rest_framework import viewsets, permissions
from apps.accounts import serializers, models


class PatientView(viewsets.ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer
