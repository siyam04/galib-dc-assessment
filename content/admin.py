from django.contrib import admin
from content.models import Category, Content


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'body', 'category', 'metadata', 'owner', 'is_public', 'created_at', 'updated_at',
        'summary', 'sentiment', 'topics', 'recommendations'
    )
    readonly_fields = ('summary', 'sentiment', 'topics', 'recommendations', 'created_at', 'updated_at')
    list_display_links = ('title',)
    list_editable = ('is_public',)
    list_filter = ('is_public', 'category', 'sentiment')
    search_fields = ('title', 'body', 'summary', 'sentiment', 'topics', 'recommendations')
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'category', 'owner', 'is_public', 'metadata')
        }),
        ('AI Analysis', {
            'fields': ('summary', 'sentiment', 'topics', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
