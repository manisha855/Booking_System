# Generated by Django 5.0.4 on 2024-06-14 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_book_city_name_book_location_book_test_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='test_type',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
