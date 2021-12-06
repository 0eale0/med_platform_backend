from apps.accounts.models import Patient, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "middle_name"]


class PatientForDoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = UserSerializer(read_only=False)
    join_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        exclude = ["link_token"]

    @staticmethod
    def get_join_link(obj):
        return f"https://site/login/{obj.link_token}"
