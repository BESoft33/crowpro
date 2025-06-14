from django.utils.timezone import datetime
from rest_framework import serializers
from users.models import User
from blog.models import Article, Editorial, Publication, PublicationAuthor


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """Serializer with dynamic field selection"""

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field in existing - allowed:
                self.fields.pop(field)


class UserSerializer(DynamicFieldsModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'profile_img', 'role', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'role', ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def get_full_name(self, obj):
        return obj.get_full_name()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationAuthor


class BaseContentSerializer(DynamicFieldsModelSerializer):
    created_by = UserSerializer(read_only=True, fields=('id', 'email', 'full_name', 'profile_img'))
    authors = UserSerializer(many=True, read_only=True, fields=('id', 'email', 'full_name', 'profile_img'))
    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self.context['request'].build_absolute_uri(obj.thumbnail.url)
        return None


class AuthorArticleSerializer(BaseContentSerializer):
    class Meta:
        model = Publication
        fields = "__all__"


class PublicationSerializer(BaseContentSerializer):
    class Meta:
        model = Publication
        fields = [
            'id', 'slug', 'title', 'content', 'thumbnail', 'thumbnail_url',
            'created_by', 'authors', 'created_on', 'updated_on',
            'published', 'published_on', 'hide', 'publication_type',
        ]
        read_only_fields = [
            'id', 'slug', 'created_on', 'updated_on',
            'thumbnail_url', 'published_on', 'hide', 'authors'
        ]
        extra_kwargs = {
            'thumbnail': {'write_only': True},
            'published': {'default': False}
        }


class ArticleSerializer(BaseContentSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 'slug', 'title', 'content', 'thumbnail_url',
            'created_by', 'authors', 'created_on', 'updated_on',
            'published', 'published_on', 'approved_by', 'approved_on',
            'hide', 'publication_type', 'thumbnail',
        ]
        read_only_fields = [
            'id', 'slug', 'created_on', 'updated_on', 'approved_on',
            'thumbnail_url', 'published_on', 'hide', 'approved_by',
            'publication_type', 'authors'
        ]
        extra_kwargs = {
            'thumbnail': {'write_only': True},
            'published': {'default': False}
        }

    def validate_published(self, value):
        if value and not self.instance.approved_by:
            raise serializers.ValidationError("Article must be approved before publishing")
        return value


class EditorialSerializer(BaseContentSerializer):
    class Meta:
        model = Editorial
        fields = [
            'id', 'slug', 'title', 'content', 'thumbnail', 'thumbnail_url',
            'created_by', 'authors', 'created_on', 'updated_on',
            'published', 'published_on', 'hide', 'publication_type',
        ]
        read_only_fields = [
            'id', 'slug', 'created_on', 'updated_on',
            'thumbnail_url', 'published_on', 'hide', 'authors'
        ]
        extra_kwargs = {
            'thumbnail': {'write_only': True},
            'published': {'default': False}
        }


class PublicationApproveSerializer(BaseContentSerializer):
    class Meta:
        model = Publication
        fields = [
            'id', 'slug', 'title', 'content', 'thumbnail_url',
            'created_by', 'created_on', 'updated_on', 'published',
            'published_on', 'hide', 'approved_by', 'approved_on', 'publication_type',
        ]
        read_only_fields = [
            'id', 'slug', 'title', 'content', 'thumbnail_url',
            'created_by', 'created_on', 'updated_on', 'published',
            'published_on', 'hide', 'publication_type',
        ]


class StatisticsSerializer(serializers.Serializer):
    total_articles = serializers.IntegerField()
    published_articles = serializers.IntegerField()
    scheduled_articles = serializers.IntegerField()
    pending_approval = serializers.IntegerField()
    active_authors = serializers.IntegerField()
    active_readers = serializers.IntegerField()
    recent_publications = serializers.ListField(child=serializers.DateTimeField())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['recent_publications'] = [
            pub.isoformat() for pub in data['recent_publications']
        ]
        return data
