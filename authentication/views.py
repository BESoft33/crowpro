from django.contrib.auth import authenticate, get_user_model

from rest_framework import exceptions
from rest_framework.decorators import permission_classes, api_view
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
                max_age= 15,  # 15 minutes until access token expire
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
                max_age=60 * 15,  # 15 minutes until expiry
                path='/'
            )

            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='none',
                max_age=60 * 60 * 24 * 30,  # 30 days
                path='/'
            )
            return response
        except TokenError as e:
            raise InvalidToken(e.args[0])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticated_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }, status=status.HTTP_200_OK)
