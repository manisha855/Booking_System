# Generated by Django 5.0.4 on 2024-06-02 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='user',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.AlterField(
            model_name='examtype',
            name='current_fee',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='examtype',
            name='newest_fee',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]