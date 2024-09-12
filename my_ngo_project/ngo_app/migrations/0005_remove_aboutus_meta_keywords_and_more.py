# Generated by Django 5.1.1 on 2024-09-10 19:40

from django_ckeditor_5.fields import CKEditor5Field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo_app', '0004_aboutus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutus',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='aboutus',
            name='video_url',
        ),
        migrations.AddField(
            model_name='aboutus',
            name='video_embed',
            field=models.TextField(blank=True, help_text='Paste the embed code for the video here'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='content',
            field=CKEditor5Field('Content'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='image',
            field=models.ImageField(help_text='Image should be 489x560 pixels', upload_to='about_us/'),
        ),
    ]
