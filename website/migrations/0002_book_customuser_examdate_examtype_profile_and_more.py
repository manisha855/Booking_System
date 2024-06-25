# Generated by Django 5.0.4 on 2024-06-25 08:52

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobileno', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('country', models.CharField(max_length=100)),
                ('address_line', models.CharField(max_length=255)),
                ('town_or_city', models.CharField(max_length=100)),
                ('passport_no', models.CharField(max_length=50)),
                ('passport_expiry_date', models.DateField()),
                ('passport_issuing_authority', models.CharField(max_length=100)),
                ('passport_file', models.FileField(upload_to='passports/')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('test_takers_first_language', models.CharField(max_length=100)),
                ('test_takers_country', models.CharField(max_length=100)),
                ('education_level', models.CharField(max_length=50)),
                ('occupation_sector', models.CharField(max_length=50)),
                ('occupation_level', models.CharField(max_length=50)),
                ('interest_in_ielts', models.CharField(max_length=50)),
                ('purpose', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city_name', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('test_mode', models.CharField(blank=True, max_length=20, null=True)),
                ('test_type', models.CharField(blank=True, max_length=200, null=True)),
                ('test_date', models.DateField(blank=True, null=True)),
                ('test_time', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('student', 'Student'), ('partner', 'Partner')], max_length=20)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('registered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrations', to='website.customuser')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ExamDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateField()),
                ('test_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(max_length=20)),
                ('test_mode', models.CharField(max_length=20)),
                ('current_fee', models.IntegerField()),
                ('newest_fee', models.IntegerField()),
                ('city_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_token', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='website.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_id', models.CharField(max_length=20, unique=True)),
                ('txn_date', models.DateField()),
                ('txn_amt', models.IntegerField()),
                ('reference_id', models.CharField(max_length=20)),
                ('remarks', models.CharField(max_length=50)),
                ('particulars', models.CharField(max_length=100)),
                ('status', models.CharField(default='PENDING', max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.AddField(
            model_name='book',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.customuser'),
        ),
        migrations.AddField(
            model_name='book',
            name='exam_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.examdate'),
        ),
        migrations.AddField(
            model_name='examdate',
            name='exam_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_dates', to='website.examtype'),
        ),
        migrations.AddField(
            model_name='book',
            name='exam_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.examtype'),
        ),
    ]