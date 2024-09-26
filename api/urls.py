from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ArticleListView,
    ArticleDetailView,
    UserListView,
    UserDetailsView,
    ArticleView,
    StatsView, AuthorArticleListView, EditorialView
)
from users.models import Editor, Author, Admin, Moderator
from .auth import IsEditor, IsAdmin, IsAuthor, IsModerator

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('article/', ArticleView.as_view(), name='article-create'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article'),
    path('editorial/', EditorialView.as_view(), name='editorial-create'),
    path('users/', UserListView.as_view(), name='users'),

    path('user/<int:pk>/', UserDetailsView.as_view(authentication_classes=[IsAuthor,
                                                                           IsAdmin,
                                                                           IsModerator
                                                                           ],
                                                   model=Author,
                                                   ), name='user'),
    path('author/<int:pk>/', UserDetailsView.as_view(authentication_classes=[IsAuthor,
                                                                             IsAdmin,
                                                                             IsModerator
                                                                             ],
                                                     model=Author,
                                                     ), name='author'),
    path('editor/<int:pk>/', UserDetailsView.as_view(authentication_classes=[IsEditor,
                                                                             IsAdmin,
                                                                             IsModerator
                                                                             ],
                                                     model=Editor,
                                                     ), name='editor'),
    path('author/articles/', AuthorArticleListView.as_view(), name='author-articles'),

    path('users/', UserListView.as_view(), name='users'),
    path('authors/', UserListView.as_view(model=Author), name='authors'),
    path('editors/', UserListView.as_view(model=Editor), name='editors'),
    path('moderators/', UserListView.as_view(model=Moderator), name='moderators'),

    path('stats/', StatsView.as_view(), name='stats'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
