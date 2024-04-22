from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'pub_date',
        'title',
        'text',
        'author',
        'location',
        'category',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'author',
        'location',
        'category',
        'is_published'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'title',
        'description',
        'slug',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'slug',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'name',
        'is_published'
    )
    list_editable = (
        'is_published',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'text',
        'is_published',
        'author',
        'post'
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'author',
        'post',
    )
