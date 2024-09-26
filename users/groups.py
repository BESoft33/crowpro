from django.contrib.auth.models import Group

USER_ROLE = ('reader', 'author', 'editor', 'moderator', 'admin',)

author_group, created = Group.objects.get_or_create('author')
editor_group, created = Group.objects.get_or_create('editor')
moderator_group, created = Group.objects.get_or_create('moderator')
admin_group, created = Group.objects.get_or_create('admin')

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

author_group.permissions.set(author_permissions)
editor_group.permissions.set(editor_permissions)
moderator_group.permissions.set(moderator_permissions)