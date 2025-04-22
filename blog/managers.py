from django.db import models
from . import models as m


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publication_type=m.Article.PublicationType.Article)


class EditorialManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publication_type=m.Article.PublicationType.Editorial)
