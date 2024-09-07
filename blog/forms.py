from django.forms import ModelForm
from .models import Article, Editorial


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'thumbnail',
        )


class EditorialForm(ModelForm):
    class Meta:
        model = Editorial
        fields = (
            'title',
            'content',
            'thumbnail',
            'hide',
        )
