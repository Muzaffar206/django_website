from django.contrib import admin
from .models import BlogPost, Category
from django_ckeditor_5.widgets import CKEditor5Widget
from django.db import models

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'categories', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'categories', 'featured_image', 'is_published', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
        js = (
            'js/custom_admin.js',
            'js/ckeditor_plugins/customblockquote/plugin.js',
        )

    def save_model(self, request, obj, form, change):
        if not obj.meta_description:
            # Create a meta description from the content if not provided
            obj.meta_description = obj.content[:157] + '...' if len(obj.content) > 160 else obj.content
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = CKEditor5Widget(config_name='extends')
        return super().formfield_for_dbfield(db_field, **kwargs)