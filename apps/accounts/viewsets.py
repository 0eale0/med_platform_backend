import random
import string
from uuid import uuid4

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transliterate import translit

from apps.accounts.models import Patient, User
from apps.accounts.serializers import BaseForPatientSerializer, UserSerializer
from apps.menus.serializers import MenuSerializer
from apps.menus.models import Menu
from apps.menus.permissions import IsDoctor, CheckUser


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

    def retrieve(self, request, *args, **kwargs):
        if "patient_id" in request.data.keys():
            patient_id = request.data["patient_id"]
        else:
            patient_id = request.user

        patient = Patient.objects.filter(user=patient_id).first()
        menu = Menu.objects.filter(user=patient_id).first()

        serialized_patient = self.serializer_class(patient).data
        serialized_menu = MenuSerializer(menu).data

        result = {'patient': serialized_patient, 'menu': serialized_menu}

        return Response(result)

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


class PatientViewForDoctor(BaseForPatientView):
    permission_classes = [IsAuthenticated & IsDoctor]


class ForPatientView(BaseForPatientView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        return Response({"error": True, "status": 403})

    def create(self, request, *args, **kwargs):
        return Response({"error": True, "status": 403})

    @CheckUser
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @CheckUser
    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, *args, **kwargs)
