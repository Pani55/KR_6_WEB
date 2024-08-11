from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'publieshed_at')
    list_filter = ('publieshed_at',)
    search_fields = ('title',)
