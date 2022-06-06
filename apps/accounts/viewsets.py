import random
import string
from uuid import uuid4

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transliterate import translit

from apps.accounts.models import Patient, User, Doctor
from apps.accounts.serializers import BaseForPatientSerializer, DoctorSerializer
from apps.menus.models import Menu
from apps.menus.permissions import IsDoctor, IsPatient, IsPersonalCabinetOwner


class BaseForPatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = BaseForPatientSerializer
    permission_classes: list

    @staticmethod
    def generate_username(fio: list) -> str:
        fio = filter(None.__ne__, fio)
        username = [translit(i, "ru", reversed=True) for i in fio]
        username = "".join(username)
        return username + str(random.randint(100, 999))

    @staticmethod
    def generate_token() -> str:
        return str(uuid4())

    @staticmethod
    def rise_data(request: dict):
        new_data = request.pop('patient')
        for item in new_data:
            request[item] = new_data[item]
        return request

    def create(self, request, *args, **kwargs):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        token = self.generate_token()
        patient_object = Patient(doctor=request.user.doctor)
        patient_object.save()
        patient_object.link_token = token
        user = User.objects.create(
            username=username,
            password=token,
            email=f'{username}@gmail.com',
        )
        user.is_active = False
        user.save()
        patient_object.user = user
        menu = Menu.objects.create()
        menu.save()
        patient_object.menu = menu
        patient_object.save()
        return Response(
            {"error": False, "invite_link": f"{request.build_absolute_uri()}{token}"}, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        request.data['user'].pop('email')
        serializer = self.get_serializer(data=self.rise_data(request.data))
        serializer.is_valid(raise_exception=False)
        user = serializer.validated_data.pop("user")
        patient_obj = get_object_or_404(Patient, id=serializer.validated_data.get("id"))
        user_obj = get_object_or_404(User, id=patient_obj.user.id)
        user_obj.first_name = user["first_name"]
        user_obj.last_name = user["last_name"]
        user_obj.middle_name = user["middle_name"]
        user_obj.save()
        serializer.update(instance=patient_obj, validated_data=serializer.validated_data)
        return Response({"error": False, "status": 200})


class PatientViewForDoctor(BaseForPatientView):
    permission_classes = [IsAuthenticated & IsDoctor]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForPatientView(BaseForPatientView):
    permission_classes = [IsAuthenticated & IsPatient]

    def destroy(self, request, *args, **kwargs):
        return Response({"error": True, "status": 403})

    def create(self, request, *args, **kwargs):
        return Response({"error": True, "status": 403})


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permissions = [IsPersonalCabinetOwner]

    def update(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user_id=request.user.id)
        doctor.contact_details = request.data["contact_details"]
        doctor.save()
        return Response({'contact_details': doctor.contact_details})

    def retrieve(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, id=kwargs["pk"])
        return Response(DoctorSerializer(doctor).data)
