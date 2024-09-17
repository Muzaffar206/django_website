# Generated by Django 5.0.6 on 2024-09-17 08:39

import ngo_app.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngo_app', '0016_remove_donation_date_donation_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='razorpay_payment_id',
            field=ngo_app.models.EncryptedField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='pan_no',
            field=ngo_app.models.EncryptedField(blank=True),
        ),
    ]
