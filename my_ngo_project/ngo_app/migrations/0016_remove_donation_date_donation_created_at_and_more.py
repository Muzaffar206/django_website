# Generated by Django 5.0.6 on 2024-09-16 19:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo_app', '0015_alter_donation_razorpay_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='date',
        ),
        migrations.AddField(
            model_name='donation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='donation',
            name='purpose',
            field=models.CharField(max_length=255),
        ),
    ]
