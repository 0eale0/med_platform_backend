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


class IsPatient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.patient == obj:
            return True


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


class IsPersonalCabinetOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.doctor and obj.user_id == request.user.id:
            return True
