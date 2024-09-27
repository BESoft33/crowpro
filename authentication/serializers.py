from rest_framework import serializers
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    serializer_class = []
    permission_classes = []
    authentication_classes = []


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'is_active')


class PasswordResetSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'new_password')
        read_only_fields = ('id', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }
