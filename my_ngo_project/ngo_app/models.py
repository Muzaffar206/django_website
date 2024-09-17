from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.models import User
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import logging
logger = logging.getLogger(__name__)

# Generate a key and store it securely (e.g., in environment variables)
# You should run this once and save the key securely
# ENCRYPTION_KEY = Fernet.generate_key()
# print(ENCRYPTION_KEY.decode())  # Save this key securely!

# In your Django settings.py:
# ENCRYPTION_KEY = 'your-securely-stored-key'

class EncryptedField(models.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.decrypt(value)

    def to_python(self, value):
        if isinstance(value, str):
            return self.decrypt(value)
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        encrypted = self.encrypt(value)
        if encrypted is None:
            logger.error(f"Encryption failed for value: {value[:4]}...")
            return None
        return encrypted
    
    @staticmethod
    def encrypt(txt):
        try:
            txt = str(txt).encode('utf-8')
            cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())
            encrypted_text = cipher_suite.encrypt(txt)
            return base64.b64encode(encrypted_text).decode('ascii')
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return None

    @staticmethod
    def decrypt(txt):
        try:
            txt = base64.b64decode(txt)
            cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())
            decoded_text = cipher_suite.decrypt(txt).decode('utf-8')
            return decoded_text
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return None

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
    pan_no = EncryptedField(blank=True, null=True)  # Now using EncryptedField
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    dofficial = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

    def save(self, *args, **kwargs):
        logger.info(f"Saving Donor with PAN: {self.pan_no[:4] if self.pan_no else 'None'}...")
        super().save(*args, **kwargs)

class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255)
    is_zakat = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    razorpay_payment_id = EncryptedField(blank=True, null=True)  # Now using EncryptedField

    def __str__(self):
        return f"Donation of {self.amount} by {self.donor}"

    def save(self, *args, **kwargs):
        logger.info(f"Saving Donation with Payment ID: {self.razorpay_payment_id[:4] if self.razorpay_payment_id else 'None'}...")
        super().save(*args, **kwargs)
