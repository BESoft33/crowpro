from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status, exceptions, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import MultiPartParser

from .serializer import (
    EditorialSerializer,
    UserSerializer,
    StatisticsSerializer,
    ArticleSerializer,
)
from .permissions import IsStaff, IsEditor, IsAuthor
from users.mixins import ActivityLogMixin
from users.models import User
from blog.models import Article, Editorial


class ArticleViewSet(GenericViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        elif self.action == 'partial_update':
            if self.request.user.role == User.Role.EDITOR:
                return ArticlePublishSerializer
            return ArticleUpdateSerializer
        return super().get_serializer_class()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, slug=None):
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer, ArticlePublishSerializer):
            if article.approved_by is None:
                raise exceptions.ValidationError("Article must be approved before publishing")
            serializer.save(published_on=timezone.now() if 'published' in request.data else None)
        else:
            serializer.save()

        return Response(serializer.data)

    def destroy(self, request, slug=None):
        article = self.get_object()
        article.hide = True
        article.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditorialViewSet(GenericViewSet):
    serializer_class = EditorialSerializer
    lookup_field = 'slug'
    permission_classes = [IsStaff]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, slug=None):
        editorial = self.get_object()
        serializer = self.get_serializer(editorial, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, permission_classes=[IsStaff])
    def list_users(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch', 'delete'])
    def manage(self, request, pk=None):
        user = self.get_object()
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
                fields=['email', 'first_name', 'last_name', 'profile_img']
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatsView(GenericViewSet):
    permission_classes = [IsStaff]
    serializer_class = StatisticsSerializer

    def list(self, request):
        stats = self.calculate_stats()
        serializer = self.get_serializer(stats)
        return Response(serializer.data)

    def calculate_stats(self):
        now = timezone.now()
        article_stats = Article.objects.aggregate(
            total_articles=Count('id'),
            published_articles=Count('id', filter=Q(published=True)),
            scheduled_articles=Count('id', filter=Q(published_on__gt=now)),
            pending_approval=Count('id', filter=Q(approved_by__isnull=True))
        )

        return {
            **article_stats,
            'active_authors': User.objects.filter(role=User.Role.AUTHOR, is_active=True).count(),
            'active_readers': User.objects.filter(role=User.Role.READER, is_active=True).count(),
            'recent_publications': Article.objects.filter(published_on__isnull=False)
                                   .order_by('-published_on')
                                   .values_list('published_on', flat=True)[:5]
        }


class PostReadOnlyViewSet(ActivityLogMixin, ReadOnlyModelViewSet):
    queryset = Article.objects.filter(hide=False, published=True)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]