from django.contrib import admin
from webapp.models import Article, Comment, Category, Tag


class CommentAdmin(admin.TabularInline):
    model = Comment
    fields = ['author', 'text']
    readonly_fields = ['author', 'text']
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author', 'category']
    search_fields = ['title', 'text']
    filter_horizontal = ['tags']
    exclude = []
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CommentAdmin]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)