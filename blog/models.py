from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django.utils.text import gettext_lazy as _
from django.core.exceptions import ValidationError

from django_ckeditor_5.fields import CKEditor5Field

from blog.managers import ArticleManager, EditorialManager
from users.models import Author, Editor, User, Writer


class Publication(models.Model):
    class PublicationType(models.TextChoices):
        Editorial = "EDITORIAL", _('Editorial')
        Article = "ARTICLE", _('Article')

    publication_type = models.TextField(choices=PublicationType.choices, default=PublicationType.Article)
    title = models.CharField(max_length=128, default='')
    published_on = models.DateTimeField(null=True, blank=True)
    content = CKEditor5Field()
    thumbnail = models.ImageField(upload_to="images/", null=True, blank=True,
                                  validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    hide = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128, unique=True, blank=True, null=True)
    authors = models.ManyToManyField(Writer, through='PublicationAuthor', related_name='publications')
    created_by = models.ForeignKey(Writer, on_delete=models.DO_NOTHING, related_name='author')
    approved_by = models.ForeignKey(to=Editor, on_delete=models.DO_NOTHING, null=True, blank=True,
                                    related_name='approved_by')
    approved_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    def clean(self):
        if self.created_by.role not in [User.Role.EDITOR, User.Role.AUTHOR]:
            raise PermissionError()


class PublicationAuthor(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    user = models.ForeignKey(Writer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Article(Publication):
    objects = ArticleManager()

    class Meta:
        proxy = True


class Editorial(Publication):
    object = EditorialManager()

    class Meta:
        proxy = True


class PublicationSeries(models.Model):
    title = models.CharField(max_length=255,)
    created_on = models.DateField(auto_now=True)
    updated_on = models.DateField(auto_now_add=True)


class PublicationSeriesChapter(models.Model):
    series = models.ForeignKey(PublicationSeries, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Publication, on_delete=models.CASCADE)


