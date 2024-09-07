from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignupView, LogoutView, LoginView, PasswordForgotView, PasswordResetView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/forgot/', PasswordForgotView.as_view(), name='password_forgot'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
]
