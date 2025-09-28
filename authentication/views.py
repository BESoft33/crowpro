from django.contrib.auth import authenticate, get_user_model

from rest_framework import exceptions
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignupSerializer, PasswordResetSerializer
from django.db import IntegrityError

import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger("authentication")
load_dotenv()
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

        response.delete_cookie(
            key='refresh',
            path='/',
            domain=None,
            samesite='None',
        )
        response.delete_cookie(
            key='access',
            path='/',
            domain=None,
            samesite='None',
        )
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
                'success': True,
                'status': status.HTTP_200_OK,
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access',
                value=str(access),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=float(os.getenv("ACCESS_TOKEN_LIFETIME")),
                path='/'
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=float(os.getenv("REFRESH_TOKEN_LIFETIME")),
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


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh", None)
        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
            access = serializer.validated_data.get("access")
            refresh = serializer.validated_data.get("refresh")
            response = Response(serializer.validated_data)

            response.set_cookie(
                key='access',
                value=str(access),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=float(os.getenv("ACCESS_TOKEN_LIFETIME")),
                path='/'
            )

            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=float(os.getenv("REFRESH_TOKEN_LIFETIME")),
                path='/'
            )
            return response
        except TokenError as e:
            raise InvalidToken(e.args[0])


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def token_verify(request):
    access_token = request.data.get("access")
    if not access_token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        token = AccessToken(access_token)
        user_id = token["user_id"]
        User.objects.get(id=user_id)
        return Response({"valid": True}, status=status.HTTP_200_OK)

    except TokenError:
        return Response({"detail": "Invalid or expired token."}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


