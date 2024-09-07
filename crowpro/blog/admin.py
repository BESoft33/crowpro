from django.contrib import admin
from .models import Article, Editorial

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'approved_by', 'published_on', 'approved_on')
    model = Article

class EditorialAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'published_on')
    model = Editorial

admin.site.register(Article, ArticleAdmin)
admin.site.register(Editorial, EditorialAdmin)