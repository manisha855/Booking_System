# Generated by Django 5.0.4 on 2024-05-07 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0032_remove_booking_user_booking_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
