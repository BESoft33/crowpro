from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
import django_filters.rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import exceptions
from django.http import Http404
from django.utils import timezone

from .filters import ArticleFilter
from .serializer import (
    EditorialSerializer,
    UserSerializer,
    ArticleUpdateSerializer,
    ArticlePublishOrApproveSerializer,
    StatisticsSerializer,
    ArticleSerializer
)
from users.mixins import ActivityLogMixin
from users.models import (
    User,
    Author,
    Editor,
    Reader,
    Moderator,
    Admin,
)
from .auth import IsEditor, IsAdmin, IsAuthor, IsModerator
from blog.models import Article, Editorial
from blog.forms import ArticleForm, EditorialForm


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ArticleFilter
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        # Optimize by selecting related fields and filtering efficiently
        queryset = super().get_queryset()
        # queryset = queryset.select_related('created_by', 'approved_by').prefetch_related('author')
        return queryset


class ArticleView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [IsAuthor, IsAdmin]

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user

            try:
                serializer = EditorialSerializer(article)
                article.save()
                return Response({
                    'message': 'Article created successfully.',
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    'message': str(e),
                    'status': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({
                'message': 'Invalid form data.',
                'errors': form.errors,
                'status': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        slug = request.query_params.get('q')
        if not slug:
            return Response({"error": "Slug is required"}, status=status.HTTP_400_BAD_REQUEST)
        article = get_object_or_404(Article, slug=slug)
        serializer = ArticleUpdateSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            # Handle thumbnail upload
            thumbnail = request.FILES.get('thumbnail')
            if thumbnail:
                serializer.validated_data['thumbnail'] = thumbnail
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        slug = request.query_params.get('q')
        if not slug:
            return Response({"error": "Slug is required"}, status=status.HTTP_400_BAD_REQUEST)
        article = get_object_or_404(Article, slug=slug)
        article.hide = True
        article.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EditorialView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [IsEditor, IsAdmin]

    def post(self, request):
        form = EditorialForm(request.POST, request.FILES)

        if form.is_valid():
            editorial = form.save(commit=False)
            editorial.created_by = request.user

            try:
                serializer = EditorialSerializer(editorial)
                editorial.save()
                return Response({
                    'message': 'Editorial created successfully.',
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    'message': str(e),
                    'status': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({
                'message': 'Invalid form data.',
                'errors': form.errors,
                'status': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        slug = request.query_params.get('q')
        if not slug:
            return Response({"error": "Slug is required"}, status=status.HTTP_400_BAD_REQUEST)
        editorial = get_object_or_404(Editorial, slug=slug)
        serializer = ArticleUpdateSerializer(editorial, data=request.data, partial=True)

        if serializer.is_valid():
            # Handle thumbnail upload
            thumbnail = request.FILES.get('thumbnail')
            if thumbnail:
                serializer.validated_data['thumbnail'] = thumbnail
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        slug = request.query_params.get('q')
        if not slug:
            return Response({"error": "Editorial not found"}, status=status.HTTP_400_BAD_REQUEST)
        editorial = get_object_or_404(Editorial, slug=slug)
        editorial.hide = True
        editorial.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorArticleListView(APIView):
    authentication_classes = [IsAuthor, IsAdmin]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        articles = Article.objects.filter(created_by=request.user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status.HTTP_200_OK)


class UserListView(GenericAPIView):
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    model = User

    def get(self, request):
        model = getattr(self, 'model', None)
        if model is None:
            raise Http404
        users = model.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


def get_object(cls, pk):
    try:
        return cls.objects.get(pk=pk)
    except cls.DoesNotExist:
        raise Http404


role_to_model = {
    'author': Author,
    'editor': Editor,
    'moderator': Moderator,
    'admin': Admin,
    'user': User,
}


class UserDetailsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    model = User

    def get(self, request, pk):
        model = getattr(self, 'model', None)
        if model is None:
            raise Http404
        user = get_object(model, pk)
        if user.is_active:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        raise User.DoesNotExist

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.user != user:
            raise PermissionError("Can't modify other user's account")
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object(User, pk)
        if request.user != user:
            raise PermissionError("Can't delete other user's account")
        serializer = UserSerializer(user, {"is_active": False}, fields=['is_active'])
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        raise exceptions.APIException()


# class ArticleRListView(ActivityLogMixin, APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({"articles": Article.objects.values()})

class PostReadOnlyViewSet(ActivityLogMixin, ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_log_message(self, request) -> str:
        return f"{request.user} is reading blog posts"


class StatsView(APIView):
    authentication_classes = [IsAdmin, IsModerator]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        today_published = Count("id", filter=Q(published_on__date=now.date()))
        this_month_published = Count("id", filter=Q(published_on__month=now.month, published_on__year=now.year))
        this_year_published = Count("id", filter=Q(published_on__year=now.year))
        total_published = Count("id", filter=Q(published=True, published_on__lte=now))
        total_scheduled = Count("id", filter=Q(published=True, published_on__gt=now, approved_by__isnull=False))
        asking_approval = Count("id", filter=Q(approved_by__isnull=False, published=True, published_on__gt=now))
        total_unapproved = Count("id", filter=Q(approved_by__isnull=True, published=True, published_on__lte=now))

        article_stats = Article.objects.aggregate(
            total_articles=Count("id"),
            total_published=total_published,
            total_scheduled=total_scheduled,
            asking_approval=asking_approval,
            total_approved=total_published,
            total_unapproved=total_unapproved,
            today_published=today_published,
            this_month_published=this_month_published,
            this_year_published=this_year_published,
        )

        active_authors_count = Author.objects.filter(is_active=True).count()
        active_readers_count = Reader.objects.filter(is_active=True).count()

        data = {
            "article": {
                "total_articles": article_stats["total_articles"],
                "total_published": article_stats["total_published"],
                "total_scheduled": article_stats["total_scheduled"],
                "asking_approval": article_stats["asking_approval"],
                "total_approved": article_stats["total_approved"],
                "total_unapproved": article_stats["total_unapproved"],
                "today_published": article_stats["today_published"],
                "this_month_published": article_stats["this_month_published"],
                "this_year_published": article_stats["this_year_published"],
            },
            "user_stats": {
                "active_authors": active_authors_count,
                "active_readers": active_readers_count,
            }
        }
        serializer = StatisticsSerializer(data)
        return Response(serializer.data)
