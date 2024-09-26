from django.forms import ModelForm
from crowpro.blog.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'thumbnail',
        )
