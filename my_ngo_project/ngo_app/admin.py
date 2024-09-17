from django.contrib import admin
from .models import Slider, AboutUs, SchemeData, Donor, Donation
from django.utils import timezone
import pytz
import logging
logger = logging.getLogger(__name__)

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

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'email', 'mobile', 'masked_pan_no')
    search_fields = ('first_name', 'surname', 'email', 'mobile')
    readonly_fields = ('masked_pan_no',)

    def masked_pan_no(self, obj):
        logger.info(f"Accessing PAN for donor {obj.id}")
        if obj.pan_no:
            logger.info(f"PAN exists for donor {obj.id}, length: {len(obj.pan_no)}")
            return '*' * (len(obj.pan_no) - 4) + obj.pan_no[-4:]
        logger.warning(f"No PAN for donor {obj.id}")
        return 'Not provided'
    masked_pan_no.short_description = 'PAN No.'

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'surname', 'email', 'mobile', 'masked_pan_no')
        }),
        ('Additional Information', {
            'fields': ('dofficial', 'address', 'city', 'country', 'state', 'pincode')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # This is an edit form
            fieldsets[0][1]['fields'] = ('first_name', 'surname', 'email', 'mobile', 'masked_pan_no', 'pan_no')
        return fieldsets

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'amount', 'purpose', 'is_zakat', 'created_at', 'paid', 'masked_payment_id')
    list_filter = ('is_zakat', 'paid', 'created_at')
    search_fields = ('donor__first_name', 'donor__surname', 'donor__email', 'purpose')
    readonly_fields = ('masked_payment_id',)

    def masked_payment_id(self, obj):
        logger.info(f"Accessing Payment ID for donation {obj.id}")
        if obj.razorpay_payment_id:
            logger.info(f"Payment ID exists for donation {obj.id}, length: {len(obj.razorpay_payment_id)}")
            return '*' * (len(obj.razorpay_payment_id) - 4) + obj.razorpay_payment_id[-4:]
        logger.warning(f"No Payment ID for donation {obj.id}")
        return 'Not provided'
    masked_payment_id.short_description = 'Razorpay Payment ID'

    fieldsets = (
        ('Donation Information', {
            'fields': ('donor', 'amount', 'purpose', 'is_zakat', 'notes', 'created_at', 'paid')
        }),
        ('Payment Information', {
            'fields': ('masked_payment_id', 'razorpay_order_id')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # This is an edit form
            fieldsets[1][1]['fields'] = ('masked_payment_id', 'razorpay_payment_id', 'razorpay_order_id')
        return fieldsets
