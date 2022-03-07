from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from apps.accounts.models import Patient, User, Doctor
from apps.accounts.serializers import ActivateUserSerializer, UserSerializer
from apps.accounts.auth import account_activation_token, send_email_activation


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uid_64, token):
        user_id = force_text(urlsafe_base64_decode(uid_64))
        user = User.objects.get(pk=user_id)

        if not account_activation_token.check_token(user, token) or user.is_active:
            return HttpResponse("user already activated")

        user.is_active = True
        user.save()

        return Response({"status": "ok"})


class ActivateUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ActivateUserSerializer

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "pass token in url params"}, status=status.HTTP_404_NOT_FOUND)
        patient = Patient.objects.filter(link_token=token).first()

        if patient is None:
            return Response({"detail": "user already active or not created"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(patient.user)
        return Response({"data": serializer.data})

    def post(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "pass token in url params"}, status=status.HTTP_404_NOT_FOUND)
        patient = Patient.objects.filter(link_token=token).first()
        user = User.objects.filter(patient=patient).first()
        if patient is None:
            return Response({"detail": "user already active or not created"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data["user"]["password"])
            user.email = serializer.validated_data["user"]["email"]
            user.first_name = serializer.validated_data["user"]["first_name"]
            user.last_name = serializer.validated_data["user"]["last_name"]
            user.middle_name = serializer.validated_data["user"]["middle_name"]
            patient.phone_number = serializer.validated_data["patient"]["phone_number"]
            patient.medical_card_number = serializer.validated_data["patient"]["medical_card_number"]
            patient.insurance_policy_number = serializer.validated_data["patient"]["insurance_policy_number"]
            patient.birth_date = serializer.validated_data["patient"]["birth_date"]
            patient.sex = serializer.validated_data["patient"]["sex"]
            patient.activity_level = serializer.validated_data["patient"]["activity_level"]
            patient.weight = serializer.validated_data["patient"]["weight"]
            patient.waist = serializer.validated_data["patient"]["waist"]
            patient.height = serializer.validated_data["patient"]["height"]
            patient.hips = serializer.validated_data["patient"]["hips"]
            patient.medical_information = serializer.validated_data["patient"]["medical_information"]
            patient.country = serializer.validated_data["patient"]["country"]
            patient.city = serializer.validated_data["patient"]["city"]
            patient.address = serializer.validated_data["patient"]["address"]
            user.is_active = False
            patient.link_token = None
            user.save()
            patient.save()
            send_email_activation(request, user)
            return Response({"status": "ok"})
        return Response({"status": "not ok"}, status=status.HTTP_404_NOT_FOUND)


class WhoAmIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.is_anonymous:
            return Response({"error": "login to view info"})
        doctor = Doctor.objects.filter(user=request.user).first()
        patient = Patient.objects.filter(user=request.user).first()
        user_serialized = self.serializer_class(request.user).data
        user_serialized["is_doctor"] = bool(doctor)
        user_serialized["is_patient"] = bool(patient)
        return Response(user_serialized)
