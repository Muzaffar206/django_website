from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.models import User

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
    content = CKEditor5Field()
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

class SchemeData(models.Model):
    scholarships = models.IntegerField(default=0)
    medical_aid = models.IntegerField(default=0)
    clinics_cases = models.IntegerField(default=0)
    sewing_machines = models.IntegerField(default=0)

    def __str__(self):
        return "Scheme Data"

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    pan_no = models.CharField(max_length=10)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    dofficial = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=200)
    is_zakat = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.donor} - {self.amount} - {self.date}"
