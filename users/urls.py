from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from . import views


# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('logout/',views.logout_view, name='logout'),
#     path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

# ]
