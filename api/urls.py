# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    EditorialViewSet,
    PostReadOnlyViewSet,
    StatsView,
    UserViewSet,
)

router = DefaultRouter()

# Register viewsets with the router
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'editorials', EditorialViewSet, basename='editorial')
router.register(r'posts', PostReadOnlyViewSet, basename='post')
router.register(r'stats', StatsView, basename='stat')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]