from django.contrib import admin
from .models import Article, Editorial, PublicationAuthor, PublicationSeries


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'get_authors', 'published_on', 'approved_on', 'approved_by',)
    model = Article

    def get_authors(self, obj):
        return ", ".join([author.get_full_name() or author.email for author in obj.authors.all()])
    get_authors.short_description = "Authors"


class EditorialAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'published_on')
    model = Editorial


class PublicationAuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors')

    def title(self, obj):
        return obj.publication.title

    def authors(self, obj):
        return obj.user


admin.site.register(Article, ArticleAdmin)
admin.site.register(Editorial, EditorialAdmin)
admin.site.register(PublicationAuthor, PublicationAuthorAdmin)
admin.site.register(PublicationSeries)
