from rest_framework import serializers
from users.models import (
    User,
)
from blog.models import Article, Editorial
from django.utils import timezone


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional fields argument
    that returns specified fields
    """

    def __init__(self, *args, **kwargs):
        # Remove the fields args before passing into the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass without fields argument
        super().__init__(*args, **kwargs)

        if fields:
            allowed_fields = set(fields)
            all_fields = set(self.fields)
            for field in all_fields - allowed_fields:
                # Remove the fields that are not in allowed_fields
                self.fields.pop(field)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }


class ArticleSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True, fields=('id', 'email', 'first_name', 'last_name', 'profile_img'))
    approved_by = UserSerializer(read_only=True, fields=('id', 'email'))
    thumbnail = serializers.ImageField()

    class Meta:
        model = Article
        fields = '__all__'


class EditorialSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True, fields=('id', 'email', 'first_name', 'last_name', 'profile_img'))
    thumbnail = serializers.ImageField()

    class Meta:
        model = Editorial
        fields = '__all__'


class ArticlePublishOrApproveSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True, fields=('id', 'first_name', 'last_name', 'profile_img'))

    def update(self, instance, validated_data):
        if 'approved_by' in validated_data and not instance.approved_by:
            instance.approved_by = validated_data['approved_by']
            instance.approved_on = timezone.now()

        if 'published' in validated_data and validated_data['published'] is True and not instance.published:
            instance.published = True
            instance.published_on = timezone.now()

        return super().update(instance, validated_data)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['title', 'content', 'slug', 'created_by', 'created_on']
        extra_kwargs = {
            'approved_by': {'write_only': True},
        }


class ArticleUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        # Update published_on if the article is published
        if validated_data.get('published', instance.published):
            instance.published_on = timezone.now()

        # Always update the updated_on field
        instance.updated_on = timezone.now()

        # Call the superclass method to handle the update
        instance = super().update(instance, validated_data)

        return instance

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'slug', 'created_by', 'created_on', 'approved_on', 'approved_by', 'hide']


class UserStatsSerializer(serializers.Serializer):
    active_authors = serializers.IntegerField()
    active_readers = serializers.IntegerField()


class ArticleStatsSerializer(serializers.Serializer):
    total_articles = serializers.IntegerField()
    total_published = serializers.IntegerField()
    total_scheduled = serializers.IntegerField()
    asking_approval = serializers.IntegerField()
    total_approved = serializers.IntegerField()
    total_unapproved = serializers.IntegerField()
    today_published = serializers.IntegerField()
    this_month_published = serializers.IntegerField()
    this_year_published = serializers.IntegerField()


class StatisticsSerializer(serializers.Serializer):
    article = ArticleStatsSerializer()
    user_stats = UserStatsSerializer()
