from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework.exceptions import AuthenticationFailed as DRFAuthFailed
from rest_framework.authentication import BaseAuthentication
from users.models import User
from .utils import get_user_from_token


def resolve_user(authorization=None):
    if authorization is None:
        return None
    return get_user_from_token(authorization)


class Author(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        if user.role == User.Role.AUTHOR:
            return user, None
        return None


class Admin(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        if user.is_superuser:
            return user, None
        return None


class Moderator(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        if user.is_staff:
            return user, None
        return None


class Editor(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        if user.role == User.Role.EDITOR:
            return user, None
        return None


class Staff(BaseAuthentication):
    def authenticate(self, request):
        user = request.user
        return (user, None) if user is not None else None


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header_token = super().authenticate(request)
        if header_token is not None:
            return header_token

        cookie_token = request.COOKIES.get('access')
        if not cookie_token:
            return None
        try:
            validated_token = self.get_validated_token(cookie_token)
            return self.get_user(validated_token), validated_token
        except InvalidToken:
            return None
