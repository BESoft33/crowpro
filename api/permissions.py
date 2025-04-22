from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from api.utils import get_user_from_token
from users.models import User


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return False if user.is_anonymous else user.role == User.Role.AUTHOR


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_anonymous or user.role == User.Role.EDITOR