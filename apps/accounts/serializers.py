from apps.accounts.models import User, Patient
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['middle_name']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['phone_number', 'medical_card_number', 'insurance_policy_number', 'birth_date', 'link_token', 'sex',
                  'activity_level', 'weight', 'waist', 'height', 'hips', 'medical_information', 'country', 'city',
                  'address', ]
