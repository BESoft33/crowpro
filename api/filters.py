from django.utils import timezone
from django_filters import rest_framework as filters
from blog.models import Article


class ArticleFilter(filters.FilterSet):
    status = filters.CharFilter(method='filter_by_status')

    class Meta:
        model = Article
        fields = ['status', 'created_by', 'approved_by']

    def filter_by_status(self, queryset, name, value):
        status_filters = {
            'published': {'published': True},
            'scheduled': {'published': False, 'published_on__gt': timezone.now()},
            'in_progress': {'published': False, 'published_on__isnull': True},
            'rejected': {'hide': True},
            'in_review': {'approved_on__isnull': True, 'hide': False, 'published': False},
        }
        return queryset.filter(**status_filters.get(value, {}))
