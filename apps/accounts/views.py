from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.auth import account_activation_token, send_email_activation
from apps.accounts.models import Patient, User, Doctor
from apps.accounts.serializers import ActivateUserSerializer, UserSerializer


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

    @staticmethod
    def get_patient_or_error(request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "pass token in url params"}, status=status.HTTP_404_NOT_FOUND), True
        patient = Patient.objects.filter(link_token=token).first()
        if patient is None:
            return Response({"detail": "user already active or not created"}, status=status.HTTP_404_NOT_FOUND), True
        return patient, False

    def get(self, request):
        patient, error = self.get_patient_or_error(request)
        if error:
            return patient
        serializer = self.serializer_class(patient.user)
        return Response({"data": serializer.data})

    def post(self, request):
        patient, error = self.get_patient_or_error(request)
        if error:
            return patient

        user = User.objects.filter(patient=patient).first()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data["user"].pop("password"))
            user.save()
            User.objects.filter(id=user.id).update(**serializer.validated_data["user"], is_active=False)
            Patient.objects.filter(id=patient.id).update(**serializer.validated_data["patient"], link_token=None)
            user.refresh_from_db()
            activate_url = send_email_activation(request, user)
            return Response({"status": f"ok {activate_url}"})
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
        user_serialized["patient_id"] = patient.pk if patient else None
        return Response(user_serialized)
