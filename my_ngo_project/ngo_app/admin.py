from django.contrib import admin
from .models import Slider, AboutUs, SchemeData

# Register your models here.

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'has_image', 'has_video')
    list_editable = ('position',)
    ordering = ('position',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'video_url', 'position')
        }),
        ('Item SEO and Accessibility', {
            'fields': ('item_description', 'item_keywords', 'image_alt_text'),
            'description': 'These fields are specific to this slider item and do not affect the entire page SEO.'
        }),
    )

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'content', 'donation_title', 'donation_content',
              'volunteer_title', 'volunteer_content', 'image', 'video_url',
              'meta_title', 'meta_description']
    # Remove 'video_embed' from the list if it's present

@admin.register(SchemeData)
class SchemeDataAdmin(admin.ModelAdmin):
    list_display = ('scholarships', 'medical_aid', 'clinics_cases', 'sewing_machines')
