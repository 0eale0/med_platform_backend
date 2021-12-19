from rest_framework import permissions


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
