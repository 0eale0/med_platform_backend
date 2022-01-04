from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from apps.accounts.models import Patient, User
from apps.accounts.serializers import PatientSelfEditSerializer
from apps.menus.permissions import IsDoctor


class ActivateUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PatientSelfEditSerializer

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"error": "pass token in url params"})
        patient = Patient.objects.filter(link_token=token).first()

        if not patient:
            return Response({"error": "user already active or not created"})
        serializer = self.serializer_class(patient)
        return Response({"data": serializer.data})

    def post(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"error": "pass token in url params"})
        patient = Patient.objects.filter(link_token=token).first()
        user = User.objects.filter(patient=patient).first()
        if not patient:
            return Response({"error": "user already active or not created"})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data.pop("user")
            user.first_name = user_data.pop("first_name")
            user.middle_name = user_data.pop("middle_name")
            user.last_name = user_data.pop("last_name")
            user.password = user_data.pop("password")
            patient.phone_number = serializer.validated_data.pop("phone_number")
            patient.medical_card_number = serializer.validated_data.pop("medical_card_number")
            patient.insurance_policy_number = serializer.validated_data.pop("insurance_policy_number")
            patient.birth_date = serializer.validated_data.pop("birth_date")
            patient.activity_level = serializer.validated_data.pop("activity_level")
            patient.weight = serializer.validated_data.pop("weight")
            patient.waist = serializer.validated_data.pop("waist")
            patient.height = serializer.validated_data.pop("height")
            patient.hips = serializer.validated_data.pop("hips")
            patient.medical_information = serializer.validated_data.pop("medical_information")
            patient.country = serializer.validated_data.pop("country")
            patient.city = serializer.validated_data.pop("city")
            patient.address = serializer.validated_data.pop("address")

            user.is_active = True
            patient.link_token = None
            user.save()
            patient.save()
            return Response({"status": "ok"})
        return Response({"status": "not ok"})
