from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin, AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView, BlacklistMixin, AccessToken):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={'status': 'success', 'message': 'Successfully logged out.'},
                            status=status.HTTP_200_OK)
        except TokenError:
            raise NotAuthenticated("Only logged in users can perform this action.")


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            raise exceptions.AuthenticationFailed('username and password required')

        user = authenticate(request, email=email, password=password)
        if user:
            refresh, access = get_tokens_for_user(user)
            user = UserSerializer(user).data
        else:
            raise exceptions.AuthenticationFailed("Email and password mismatch.")
        return Response({
            'access': access,
            'refresh': refresh,
            'user': user,
            'status': status.HTTP_200_OK
        })


class PasswordForgotView(APIView):
    pass


class PasswordResetView(APIView):
    authentication_classes = [JWTAuthentication]
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
