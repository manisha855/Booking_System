# Generated by Django 5.0.4 on 2024-05-24 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0042_alter_profile_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.customuser'),
        ),
    ]