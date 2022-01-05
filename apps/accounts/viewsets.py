import random
from uuid import uuid4

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transliterate import translit

from apps.accounts.models import Patient, User
from apps.accounts.serializers import PatientForDoctorSerializer
from apps.menus.permissions import IsDoctor


class PatientViewForDoctor(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientForDoctorSerializer
    permission_classes = [IsAuthenticated & IsDoctor]

    @staticmethod
    def generate_username(fio: list) -> str:
        fio = filter(None.__ne__, fio)
        username = [translit(i, "ru", reversed=True) for i in fio]
        username = "".join(username)
        return username + str(random.randint(100, 999))

    @staticmethod
    def generate_token() -> str:
        return str(uuid4())

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update(
            {
                "user": {
                    "first_name": data.pop("first_name"),
                    "middle_name": data.pop("middle_name"),
                    "last_name": data.pop("last_name"),
                },
                "doctor": request.user.id,
            }
        )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop("user")
        first_name = user.pop("first_name")
        middle_name = user.pop("middle_name")
        last_name = user.pop("last_name")
        username = self.generate_username(fio=[first_name, middle_name, last_name])
        token = self.generate_token()
        patient_object = serializer.save()
        patient_object.link_token = token
        user = User.objects.create(
            username=username,
            password=token,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            email=f'{username}@gmail.com',
        )
        user.is_active = False
        user.save()
        patient_object.user = user
        patient_object.save()
        return Response({"error": False, "status": 200})

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop("user")
        user_obj = get_object_or_404(User, id=user.get("id"))
        user_obj.first_name = user["first_name"]
        user_obj.last_name = user["last_name"]
        user_obj.middle_name = user["middle_name"]
        user_obj.save()
        patient_obj = get_object_or_404(Patient, id=serializer.validated_data.get("id"))
        serializer.update(instance=patient_obj, validated_data=serializer.validated_data)
        return Response({"error": False, "status": 200})
