from apps.accounts.models import Patient, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name"]


class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name", "email", "password"]


class PatientForDoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    join_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        exclude = ["link_token"]

    @staticmethod
    def get_join_link(obj):
        return f"{obj.link_token}"


class ActivateUserSerializer(serializers.ModelSerializer):
    user = AllUsersSerializer(read_only=False)

    class Meta:
        model = Patient
        exclude = ["link_token", "doctor", "menu"]
        read_only_fields = ('first_name', 'last_name', 'middle_name')
