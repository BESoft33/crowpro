from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, exceptions, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, OR
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView

from .serializer import (
    EditorialSerializer,
    UserSerializer,
    StatisticsSerializer,
    ArticleSerializer,
    PublicationApproveSerializer, PublicationSerializer
)
from .permissions import IsStaff, IsEditor, IsAuthor
from users.models import User
from blog.models import Article, Editorial, Publication


class AuthorArticleView(APIView):
    def get(self, request):
        queryset = Article.objects.filter(authors=request.user).distinct()
        serializer = ArticleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class AuthorPublicationView(APIView):
    permission_classes = []

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        queryset = Publication.objects.filter(
            published=True,
            authors=user
        ).distinct()

        serializer = PublicationSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ArticleViewSet(GenericViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Article.objects.all()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(hide=False)
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, authors=request.user)
        serializer.instance.authors.set([request.user])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'published' in request.data:
            if instance.approved_by is None:
                raise exceptions.ValidationError("Article must be approved before publishing.")
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

    @action(detail=True, methods=["patch"], url_path="update-authors")
    def update_authors(self, request, slug=None):
        article = self.get_object()

        if request.user != article.created_by:
            return Response({"detail": "Only the creator can update authors."}, status=403)

        author_ids = request.data.get("author_ids", [])
        if not isinstance(author_ids, list):
            return Response({"detail": "author_ids must be a list."}, status=400)

        users = User.objects.filter(id__in=author_ids, role__in=[User.Role.AUTHOR, User.Role.EDITOR])
        if users.count() != len(author_ids):
            return Response({"detail": "Invalid or disallowed user IDs."}, status=400)

        article.authors.set(users)
        return Response({"detail": "Authors updated successfully."})


class EditorialViewSet(GenericViewSet):
    serializer_class = EditorialSerializer
    lookup_field = 'slug'
    queryset = Editorial.objects.filter(published=True)

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
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user,
                            publication_type=Publication.PublicationType.Editorial)

            serializer.instance.authors.set([request.user.id])

            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def partial_update(self, request, slug=None):
        editorial = self.get_object()
        serializer = self.get_serializer(editorial, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PublicationUpdateView(RetrieveUpdateAPIView):
    serializer_class = PublicationApproveSerializer
    permission_classes = [IsEditor]
    queryset = Publication.objects.filter(hide=False)
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

    def get_permissions(self, ):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

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
            if request.user is not user:
                raise PermissionError("You cannot update other user's info")

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

    @action(detail=False, url_path='authors')
    def active_authors(self, request):
        users = User.objects.filter(role=User.Role.AUTHOR, is_active=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='readers')
    def active_readers(self, request):
        users = User.objects.filter(role=User.Role.READER, is_active=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class StatsView(ListAPIView):
    permission_classes = [IsStaff]

    def list(self, request, *args, **kwargs):
        now = timezone.now()
        today = now.date()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        article_stats = {
            "total_articles": Article.objects.count(),
            "total_published": Article.objects.filter(published=True).count(),
            "total_scheduled": Article.objects.filter(published_on__gt=now).count(),
            "asking_approval": Article.objects.filter(approved_by__isnull=True).count(),
            "total_approved": Article.objects.filter(approved_by__isnull=False).count(),
            "total_unapproved": Article.objects.filter(approved_by__isnull=True).count(),
            "today_published": Article.objects.filter(published_on__date=today).count(),
            "this_month_published": Article.objects.filter(published_on__gte=month_start).count(),
            "this_year_published": Article.objects.filter(published_on__gte=year_start).count(),
        }

        user_stats = {
            "active_authors": User.objects.filter(role=User.Role.AUTHOR, is_active=True).count(),
            "active_readers": User.objects.filter(role=User.Role.READER, is_active=True).count(),
        }

        return Response({
            "article": article_stats,
            "user_stats": user_stats,
        })


class PostReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Publication.objects.filter(hide=False, published=True)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    @action(detail=False, url_path='articles/all')
    def all_articles(self, request):
        queryset = Article.objects.defer('content')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='articles/published')
    def published(self, request):
        queryset = Article.objects.filter(published=True, hide=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='articles/scheduled')
    def scheduled(self, request):
        queryset = Article.objects.filter(published_on__gt=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='articles/unapproved')
    def asking_approval(self, request):
        queryset = Article.objects.filter(published=True, approved_by__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='articles/approved')
    def approved(self, request):
        queryset = Article.objects.filter(approved_by__isnull=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='published/today')
    def published_today(self, request):
        today = timezone.now().date()
        queryset = Article.objects.filter(published_on__date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='published/current-month')
    def published_this_month(self, request):
        now = timezone.now()
        queryset = Article.objects.filter(published_on__year=now.year, published_on__month=now.month)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='published/current-year')
    def published_this_year(self, request):
        now = timezone.now()
        queryset = Article.objects.filter(published_on__year=now.year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
