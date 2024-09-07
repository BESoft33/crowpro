from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

from .models import ActivityLog, LOGIN, LOGIN_FAILED
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )


def get_client_user_agent(request):
    user_agent = request.headers.get("User-Agent")
    return user_agent


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user.get_full_name()} ({user.id}) is logged in with ip:{get_client_ip(request)}"
    ActivityLog.objects.create(actor=user, action_type=LOGIN, remarks=message)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for email {credentials.get('email')} with ip: {get_client_ip(request)}, user agent {get_client_user_agent(request)}"
    ActivityLog.objects.create(action_type=LOGIN_FAILED, remarks=message)


author_permissions = [
    ('can_add_article', 'Can create an Article'),
    ('can_view_article', 'Can view an Article'),
    ('can_publish_article', 'Can publish an Article'),
    ('can_schedule_publish_article', 'Can schedule an Article to publish')
]

editor_permissions = [
    ('can_add_editorial', 'Can create an Editorial'),
    ('can_change_editorial', 'Can modify an Editorial'),
    ('can_view_editorial', 'Can view an Editorial'),
    ('can_delete_editorial', 'Can delete an Editorial'),
    ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'),
    ('can_change_article', 'Can update an Article'),
    ('can_view_article', 'Can view an Article'),
    ('can_approve_article', 'Can approve an Article to publish'),
    ('can_schedule_publish_article', 'Can schedule an Article to publish'),
    ('can_view_author', 'Can view the author of article')
]

moderator_permissions = [
    ('can_add_editorial', 'Can create an Editorial'),
    ('can_change_editorial', 'Can modify an Editorial'),
    ('can_view_editorial', 'Can view an Editorial'),
    ('can_delete_editorial', 'Can delete an Editorial'),
    ('can_schedule_publish_editorial', 'Can schedule the Editorial to publish'),
    ('can_change_article', 'Can update an Article'),
    ('can_view_article', 'Can view an Article'),
    ('can_delete_article', 'Can delete an Article'),
    ('can_approve_article', 'Can approve an Article to publish'),
    ('can_schedule_publish_article', 'Can schedule an Article to publish'),
    ('can_view_author', 'Can view the author of article'),
    ('can_delete_author', 'Can delete the author'),
]


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    groups_permissions = {
        'Moderators': moderator_permissions,
        'Authors': author_permissions,
        'Editors': editor_permissions,
    }

    for name, permission in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=name)

        # Clear existing permissions to ensure we start fresh
        group.permissions.clear()

        # Iterate over all models in the app
        # Generate the codename for each permission
        try:
            # Retrieve the permission
            permission = Permission.objects.get(codename=permission)
            # Add the permission to the group
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            pass
