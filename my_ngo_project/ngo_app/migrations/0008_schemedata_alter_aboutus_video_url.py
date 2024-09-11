# Generated by Django 5.1.1 on 2024-09-11 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo_app', '0007_remove_aboutus_video_embed_alter_aboutus_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scholarships', models.IntegerField(default=0)),
                ('medical_aid', models.IntegerField(default=0)),
                ('clinics_cases', models.IntegerField(default=0)),
                ('sewing_machines', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Scheme Data',
                'verbose_name_plural': 'Scheme Data',
            },
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='video_url',
            field=models.URLField(blank=True, help_text='URL of the YouTube video (embed URL)'),
        ),
    ]
