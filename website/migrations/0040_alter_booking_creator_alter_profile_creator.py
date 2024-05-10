# Generated by Django 5.0.4 on 2024-05-10 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0039_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.customuser'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='website.customuser'),
        ),
    ]
