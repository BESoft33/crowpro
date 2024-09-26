from django.contrib import admin
from .models import *


# Register your models here.
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    model = Author


class EditorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    model = Editor


class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    model = Moderator


class Administrator(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    model = Admin


class ReaderAdmin(admin.ModelAdmin):
    model = Reader
    list_display = ('first_name', 'last_name', 'email', 'role')


admin.site.register(Author, BloggerAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Admin, Administrator)
admin.site.register(User)

admin.site.register(ActivityLog)
