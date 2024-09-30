from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from stdimage import StdImageField
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

def featured_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a new filename using the slug and extension
    filename = f"{instance.slug}.{ext}"
    # Return the complete path
    return os.path.join('blog_images', filename)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = CKEditor5Field('Content', config_name='extends')
    categories = models.ManyToManyField('Category')
    featured_image = models.ImageField(upload_to=featured_image_path, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    tags = TaggableManager()

    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_description:
            # Create a meta description from the content if not provided
            self.meta_description = self.content[:157] + '...' if len(self.content) > 160 else self.content
        if self.featured_image:
            img = Image.open(self.featured_image)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Convert to RGB if the image has an alpha channel or is in palette mode
                img = img.convert('RGB')
            img.thumbnail((370, 256), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            # Use the new filename format
            new_name = f"{self.slug}.jpg"
            self.featured_image.save(new_name, ContentFile(output.read()), save=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_detail', kwargs={'slug': self.slug})