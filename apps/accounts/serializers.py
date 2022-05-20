from rest_framework import serializers

from apps.accounts.models import Patient, User, Doctor


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name", "email", "password"]
        write_only_fields = ["password"]


class BaseForPatientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = UserSerializer(read_only=False)
    join_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        exclude = ["link_token"]

    @staticmethod
    def get_join_link(obj):
        return f"{obj.link_token}"


class ActivatePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ["link_token", "doctor", "menu"]


class ActivateUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    patient = ActivatePatientSerializer(read_only=False)

    class Meta:
        model = Patient
        fields = ["user", "patient"]


class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        result = UserSerializer(User.objects.filter(id=obj.user.id).first()).data
        del result['password']
        return result

    class Meta:
        model = Doctor
        fields = ['user', 'post', 'contact_details']
