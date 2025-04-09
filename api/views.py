from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status, exceptions, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, OR
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.generics import UpdateAPIView

from .serializer import (
    EditorialSerializer,
    UserSerializer,
    StatisticsSerializer,
    ArticleSerializer,
    PublicationApproveSerializer
)
from .permissions import IsStaff, IsEditor, IsAuthor
from users.models import User
from blog.models import Article, Editorial, Publication


class ArticleViewSet(GenericViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthor()]

    def get_queryset(self):
        queryset = Article.objects.all()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(hide=False)
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if instance.approved_by is None:
            raise exceptions.ValidationError("Article must be approved before publishing.")
        # Check if 'published' is in the request data to determine publishing
        if 'published' in request.data:
            published_on = timezone.now() if request.data['published'] else None
            serializer.save(published_on=published_on)
        else:
            serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hide = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditorialViewSet(GenericViewSet):
    serializer_class = EditorialSerializer
    lookup_field = 'slug'
    queryset = Editorial.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsEditor()]
        return [IsStaff()]

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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


class PublicationUpdateView(UpdateAPIView):
    serializer_class = PublicationApproveSerializer
    permission_classes = [IsEditor]
    queryset = Publication.objects.all()
    lookup_field = 'slug'

    def perform_update(self, serializer):
        instance = serializer.instance
        if 'approved_by' in serializer.validated_data:
            if not instance.approved_by:
                serializer.validated_data['approved_on'] = timezone.now()
                serializer.save()
            else:
                raise ValidationError("This publication was already approved.")


class UserViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self,):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [IsAuthenticated()]

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
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

    def destroy(self):
        user = self.request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)


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


class PostReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.filter(hide=False, published=True)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
