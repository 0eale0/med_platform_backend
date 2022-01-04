from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from apps.accounts.models import Patient, User
from apps.accounts.serializers import ActivateUserSerializer


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
            user.set_password(serializer.validated_data.pop("password"))
            user.email = serializer.validated_data.pop("email")
            user.is_active = True
            patient.link_token = None
            user.save()
            patient.save()
            return Response({"status": "ok"})
        return Response({"status": "not ok"}, status=status.HTTP_404_NOT_FOUND)
