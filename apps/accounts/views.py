from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from apps.accounts.models import Patient, User
from apps.accounts.serializers import ActivateUserSerializer
from apps.menus.permissions import IsDoctor


class ActivateUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ActivateUserSerializer

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"error": "pass token in url params"})
        patient = Patient.objects.filter(link_token=token).first()

        if not patient:
            return Response({"error": "user already active or not created"})
        serializer = self.serializer_class(patient.user)
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
            user.password = serializer.validated_data.pop("password")
            user.email = serializer.validated_data.pop("email")
            user.is_active = True
            patient.link_token = None
            user.save()
            patient.save()
            return Response({"status": "ok"})
        return Response({"status": "not ok"})
