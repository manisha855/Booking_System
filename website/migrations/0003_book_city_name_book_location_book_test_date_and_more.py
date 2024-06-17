# Generated by Django 5.0.4 on 2024-06-14 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_book_customuser_examtype_transaction_delete_record_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='city_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='test_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='test_mode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='test_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
