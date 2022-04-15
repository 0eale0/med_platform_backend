from rest_framework import permissions
from rest_framework.response import Response

from apps.accounts.models import Patient


class IsOwnerOrReadOnlyDay(permissions.BasePermission):
    "если ты доктор делай что хочешь, если пациент, то только смеотреть или менять в своем дне"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.doctor:
            return True

        if request.user.patient:
            if view.action == "destroy":
                return False

            if request.user.patient.menu == obj.menu:
                return True
            return False


class IsDoctor(permissions.BasePermission):
    "если ты доктор делай что хочешь, если пациент, то только смотри"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.doctor:
            return True


class CheckUser:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        data = request.data

        if "user" in data.keys():
            user_from_data = data["user"]
        else:
            return Response({"error": "user_id not in request.data", "status": 400})

        user_id_from = request.user

        if user_id_from != user_from_data:
            return Response({"error": True, "status": 403})

        self.func(request, *args, **kwargs)


class IsDayOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False

        if request.method not in permissions.SAFE_METHODS:
            return False

        patient = Patient.objects.filter(user_id=request.user.id).first()
        if not patient:
            return False

        if patient.menu == obj.day.menu:
            return True
        return False
