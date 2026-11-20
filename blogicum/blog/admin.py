from django.contrib import admin

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка отображения публикаций в панели администратора."""

    list_display = (
        'title',
        'pub_date',
        'author',
        'category',
        'location',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
        'category',
    )
    search_fields = ('title', 'text')
    list_filter = ('category', 'is_published')
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в панели администратора."""

    list_display = (
        'title',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'description')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Настройка отображения местоположений в панели администратора."""

    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
