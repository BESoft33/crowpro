from django.contrib.auth import models
from django.db.models.query import QuerySet
from django.db.models import Q
from . import models as user_models


class UserManager(models.BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email is a required field.")
        if not password:
            raise ValueError("Password is a required field.")
        if not first_name:
            raise ValueError("First Name is a required field.")
        if not last_name:
            raise ValueError("Last Name is a required field.")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', user_models.User.Role.ADMIN)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_staffuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', user_models.User.Role.MODERATOR)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('role', user_models.User.Role.READER)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class EditorManager(models.UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=user_models.User.Role.EDITOR, is_active=True)


class AuthorManager(models.UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=user_models.User.Role.AUTHOR, is_active=True)


class ModeratorManager(models.UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(Q(is_staff=True) | Q(user_models.User.Role.MODERATOR))


class AdminManager(models.UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(role=user_models.User.Role.ADMIN, is_active=True)


class ReaderManager(models.UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(role=user_models.User.Role.READER, is_active=True)
