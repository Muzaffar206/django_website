from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from urllib.parse import urlparse, parse_qs

def validate_image_size(image):
    if image and (image.width != 1280 or image.height != 720):
        raise ValidationError("Image must be 1280x720 pixels.")

class Slider(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='slider_images/', validators=[validate_image_size], blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # SEO fields for the slider item
    item_description = models.CharField(max_length=160, blank=True, help_text="Description of this slider item (for accessibility and SEO)")
    item_keywords = models.CharField(max_length=255, blank=True, help_text="Keywords/tags for this slider item")
    image_alt_text = models.CharField(max_length=100, blank=True, help_text="Alternative text for the image")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def clean(self):
        if Slider.objects.count() >= 5 and not self.pk:
            raise ValidationError("You can only have a maximum of 5 slider items.")
        if not self.image and not self.video_url:
            raise ValidationError("You must provide either an image or a video URL.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = RichTextField()
    donation_title = models.CharField(max_length=100)
    donation_content = models.TextField()
    volunteer_title = models.CharField(max_length=100)
    volunteer_content = models.TextField()
    image = models.ImageField(upload_to='about_us/', help_text="Image should be 489x560 pixels")
    video_url = models.URLField(blank=True, help_text="URL of the YouTube video (embed URL)")
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO Meta Title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO Meta Description")

    def get_youtube_embed_url(self):
        if not self.video_url:
            return ''
        
        parsed_url = urlparse(self.video_url)
        
        if 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtube.com' in parsed_url.netloc:
            query = parse_qs(parsed_url.query)
            video_id = query.get('v', [''])[0]
            return f"https://www.youtube.com/embed/{video_id}" if video_id else ''
        else:
            return ''

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About Us"
