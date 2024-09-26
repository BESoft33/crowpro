from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify

from django_ckeditor_5.fields import CKEditor5Field

from users.models import Author, Editor


class Article(models.Model):
    title = models.CharField(max_length=128, default='')
    published_on = models.DateTimeField(null=True, blank=True)
    content = CKEditor5Field()
    thumbnail = models.ImageField(upload_to="images/", null=True, blank=True,
                                  validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    hide = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(to=Author, on_delete=models.DO_NOTHING, related_name='author')
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


class Editorial(models.Model):
    title = models.CharField(max_length=255)
    content = CKEditor5Field()
    thumbnail = models.ImageField(upload_to="images/", null=True, blank=True,
                                  validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    slug = models.SlugField(max_length=128, unique=True)
    hide = models.BooleanField(default=False)
    created_by = models.ForeignKey(to=Editor, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    last_update_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.created_by} - {self.title}"

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)
