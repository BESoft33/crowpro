from users.models import User
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


def get_user_from_token(authorization):
    if authorization.startswith('Bearer'):
        token = authorization.split(' ')[1]
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            return user
        except TokenError:
            raise exceptions.AuthenticationFailed("Session expired. Login again to continue.")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Authentication credentials invalid. Please try again.")
    else:
        raise exceptions.AuthenticationFailed("Bearer token not found.")
