from django.urls import path, include

from .views import (SignupView,
                    LogoutView,
                    LoginView,
                    PasswordForgotView,
                    PasswordResetView,
                    authenticated_user,
                    CookieTokenRefreshView)

urlpatterns = [
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/forgot/', PasswordForgotView.as_view(), name='password_forgot'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('current_user/', authenticated_user, name='current_user'),
]
