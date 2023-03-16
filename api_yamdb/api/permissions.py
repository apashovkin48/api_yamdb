from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.role == User.ADMIN
            )
