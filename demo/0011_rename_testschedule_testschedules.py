# Generated by Django 5.0.4 on 2024-04-24 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_testschedule_exam_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestSchedule',
            new_name='TestSchedules',
        ),
    ]