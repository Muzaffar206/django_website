from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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
