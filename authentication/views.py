from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin, AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import SignupSerializer, UserSerializer, PasswordResetSerializer
from django.db import IntegrityError
from .utils import get_tokens_for_user

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'redirect_url': 'login', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'status': 'error', 'message': 'An account with the provided email address already exists.'},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        response = Response({
            'status': 'success',
            'message': 'Successfully logged out.'
        }, status=status.HTTP_200_OK)

        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise exceptions.AuthenticationFailed('Username and password required')

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            response = Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'status': status.HTTP_200_OK,
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access',
                value=str(access),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=60 * 15,  # 15 minutes until access token expire
                path='/'
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=60 * 60 * 24 * 30,  # 30 days until refresh token expire
                path='/'
            )
            return response

        raise exceptions.AuthenticationFailed("Invalid credentials")


class PasswordForgotView(APIView):
    pass


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = authenticate(request, email=request.data['email'], password=request.data['password'])
        if user is None:
            raise AuthenticationFailed()
        if user == request.user:
            if user.check_password(request.data['new_password']):
                raise PermissionDenied("Cannot use current password as a new password.")
            serializer = PasswordResetSerializer(user, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            raise PermissionDenied()


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_current_user(request):
    access_token = request.COOKIES.get('access')
    refresh_token = request.COOKIES.get('refresh')

    if access_token:
        try:
            access = AccessToken(access_token)
            user_id = access.get('user_id')
            user = User.objects.get(id=user_id)
            return Response(UserSerializer(user).data)
        except TokenError:
            pass
        except User.DoesNotExist:
            raise NotAuthenticated("User not found.")

    # Access token is not found or invalid, regenerate a new access token
    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh.get('user_id')
            user = User.objects.get(id=user_id)

            new_access_token = str(refresh.access_token)

            response = Response(UserSerializer(user).data)
            response.set_cookie(
                'access',
                new_access_token,
                httponly=True,
                secure=True,
                samesite=None,
                max_age=60 * 15,
                path='/'
            )

            response.set_cookie(
                'refresh',
                refresh,
                httponly=True,
                secure=True,
                max_age=60*60*24*30,
                path='/',
            )
            return response
        except TokenError:
            raise NotAuthenticated("Invalid token.")
        except User.DoesNotExist:
            raise NotAuthenticated("User not found.")

    # Token verification failed
    raise NotAuthenticated("You are not signed in.")
