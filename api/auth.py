from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions, status
from users.models import User
from rest_framework.response import Response

from .utils import get_user_from_token


def resolve_user(authorization=None):
    if authorization is None:
        raise exceptions.NotAuthenticated()
    return get_user_from_token(authorization)


class IsAuthor(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.role == User.Role.AUTHOR:
            return user, None
        return None


class IsAdmin(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.is_superuser:
            return user, None
        return None


class IsModerator(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.is_staff:
            return user, None
        return None


class IsEditor(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.role == User.Role.EDITOR:
            return user, None
        return None
