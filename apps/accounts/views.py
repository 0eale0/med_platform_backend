from uuid import uuid4

from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Patient, User, Doctor
from apps.accounts.serializers import (
    ActivateUserSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    SendEmailResetPasswordSerializer,
)
from utils.emails import send_activate_user_email, send_reset_password_email
from utils.functions import get_dict_with_changes
from apps.menus.permissions import IsDoctor, IsPatient, PatientDoctorOrPatient


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        patient = Patient.objects.get(user_activate_token=token)
        user = patient.user

        if not user or user.is_active:
            return HttpResponse("Пользователь уже активирован")

        patient.user_activate_token = None
        patient.save()
        user.is_active = True
        user.save()

        return Response({"status": "ok"})


class SendEmailResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SendEmailResetPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        patient = Patient.objects.filter(user=user.pk).first()

        if not user:
            return (
                Response(
                    {"detail": "Пользователя с такой электронной почтой не существует"},
                    status=status.HTTP_404_NOT_FOUND,
                ),
                True,
            )

        password_reset_token = str(uuid4())
        patient.password_reset_token = password_reset_token
        patient.save()

        domain = f"{request.scheme}://{request.META['HTTP_HOST']}"

        send_reset_password_email(domain, user.email, password_reset_token)

        return Response({"status": "ok"})


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    @staticmethod
    def get_patient_or_error(token):
        patient = Patient.objects.filter(password_reset_token=token).first()
        if patient is None:
            return (
                Response({"detail": "Ссылка более недействительна"}, status=status.HTTP_404_NOT_FOUND),
                True,
            )
        return patient, False

    def post(self, request, token):
        patient, error = self.get_patient_or_error(token)
        if error:
            return patient

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            password = serializer.validated_data.pop("password")

            patient.password_reset_token = None
            patient.save()

            user = patient.user
            user.set_password(password)
            user.save()

            return Response({"status": "ok"})

        return Response({"status": "not ok"})


class ActivateUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ActivateUserSerializer

    @staticmethod
    def get_patient_or_error(request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Укажите токен в параметрах ссылки"}, status=status.HTTP_404_NOT_FOUND), True
        patient = Patient.objects.filter(user_activate_token=token).first()
        if patient is None:
            return (
                Response(
                    {"detail": "Пользователь уже активирован или не существует"}, status=status.HTTP_404_NOT_FOUND
                ),
                True,
            )
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
        if serializer.is_valid(raise_exception=False):
            user.set_password(serializer.validated_data["user"].pop("password"))
            user.save()
            email_token = str(uuid4())
            try:
                User.objects.filter(id=user.id).update(**serializer.validated_data["user"], is_active=False)
                Patient.objects.filter(id=patient.id).update(
                    **serializer.validated_data["patient"], user_activate_token=email_token
                )
                user.refresh_from_db()

                domain = f"{request.scheme}://{request.META['HTTP_HOST']}"
                send_activate_user_email(domain, user.email, user.patient.user_activate_token)
                return Response({"status": "ok"})
            except IntegrityError:
                return Response(
                    {"status": "not ok", 'detail': 'Пользователь с таким email уже существует'},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response({"status": "not ok"}, status=status.HTTP_404_NOT_FOUND)


class WhoAmIView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = UserSerializer

    def get(self, request):
        send_reset_password_email("hh.ru", "ff@mail.ru", "dadsas")

        if request.user.is_anonymous:
            return Response({"error": "Войдите в аккаунт, чтобы увидеть информацию"})
        doctor = Doctor.objects.filter(user=request.user).first()
        patient = Patient.objects.filter(user=request.user).first()
        user_serialized = self.serializer_class(request.user).data
        if hasattr(request.user, 'doctor'):
            user_serialized["contact_details"] = request.user.doctor.contact_details
        user_serialized["is_doctor"] = bool(doctor)
        user_serialized["is_patient"] = bool(patient)
        user_serialized["patient_id"] = patient.pk if patient else None

        return Response(user_serialized)


class ObjectHistory(APIView):
    permission_classes = [IsDoctor & IsPatient]

    allowed_models_for_history = {"patient": Patient}
    allowed_fields_for_history = {"patient": {"height", "weight", "city"}}  # if model not in dict return all fields
    MAX_COUNT_TO_RETURN = 5

    def get(self, request, model, pk):
        if model not in self.allowed_models_for_history.keys():
            return Response(
                {"status": "not ok", "error": "Данная модель не имеет истории изменений"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        model_class = self.allowed_models_for_history[model]
        fields = self.allowed_fields_for_history.get(model, [field.name for field in model_class._meta.get_fields()])
        doctor = Doctor.objects.filter(user=request.user.pk).first()

        if doctor:
            object_to_check_history = model_class.objects.filter(user=pk).first()
        else:
            object_to_check_history = Patient.objects.filter(user=request.user).first()

        if not object_to_check_history:
            return Response(
                {"status": "not ok", "error": "Такого пользователя нет в системе"}, status=status.HTTP_400_BAD_REQUEST
            )

        dict_with_changes = get_dict_with_changes(object_to_check_history, self.MAX_COUNT_TO_RETURN, fields)

        return Response(dict_with_changes)


class CalculateCPFC(APIView):
    permission_classes = [
        PatientDoctorOrPatient,
    ]
    queryset = Patient.objects.all()

    def post(self, request, pk):
        patient = Patient.objects.get(id=pk)
        self.check_object_permissions(self.request, patient)
        if patient:
            patient.set_cpfc()
        return Response({"status": "ok"})


class GetDoctor(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request):
        if request.user.is_anonymous:
            return Response({"error": "Войдите в аккаунт, чтобы увидеть информацию"})
        contact_details = request.user.patient.doctor.contact_details
        return Response({"contact": contact_details})
