from rest_framework.authentication import BaseAuthentication
from users.models import User
from .utils import get_user_from_token




def resolve_user(authorization=None):
    if authorization is None:
        return None
    return get_user_from_token(authorization)


class Author(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.role == User.Role.AUTHOR:
            return user, None
        return None


class Admin(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.is_superuser:
            return user, None
        return None


class Moderator(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.is_staff:
            return user, None
        return None


class Editor(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        if user.role == User.Role.EDITOR:
            return user, None
        return None


class Staff(BaseAuthentication):
    def authenticate(self, request):
        user = resolve_user(request.headers.get('Authorization'))
        return (user, None) if user.is_staff else None
