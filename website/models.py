from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('individual', 'Individual'),
        ('partner', 'Partner')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# Add related_name to resolve the clash for groups and user_permissions
CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'

class Booking(models.Model):
    name = models.CharField(max_length=100)
    passport = models.CharField(max_length=100)
    test_city = models.CharField(max_length=100, choices=[('ktm', 'Kathmandu')])
    signature = models.FileField(upload_to='signatures/')
    signature_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    test_model = models.CharField(max_length=20, choices=[('academic', 'Academic'), ('general', 'General Training')])
    delivery_method = models.CharField(max_length=20, choices=[('computer', 'Computer-delivered'), ('paper', 'Paper-based')])
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking -> {self.name}"
    
class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/')
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    student_id = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    batch = models.CharField(max_length=20)
    major = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile -> {self.full_name}"

#Exam Tyes set by admin
class ExamType(models.Model):
    TEST_TYPE_CHOICES = [
        ('paper', 'IELTS on Paper'),
        ('computer', 'IELTS on Computer'),
        ('visa', 'IELTS for Visas and Immigration'),
        ('lifeskill', 'IELTS Life Skills'),
    ]
    TEST_MODEL_CHOICES = [
        ('academic', 'Academic'),
        ('general', 'General Training'),
    ]

    city_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    current_fee = models.IntegerField()
    newest_fee = models.IntegerField()
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    test_model = models.CharField(max_length=20, choices=TEST_MODEL_CHOICES)

    def __str__(self):
        return f"{self.get_test_type_display()} - {self.test_model} - {self.city_name}"
    
    def __str__(self):
        return f"{self.city_name} ExamType"
    
# for testschedule  by admin  
class TestSchedules(models.Model):
    TEST_TYPES = (
        ('LRW', 'LRW'),
        ('Listening', 'Listening'),
    )

    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.test_type} test on {self.date} ({self.start_time} - {self.end_time}) at ({self.exam_type})"

    @property
    def exam_type_choices(self):
        return self.exam_type.TEST_TYPE_CHOICES



#model for partner
# class Partner(models.Model):
#     create_at = models.DateTimeField(auto_now_add=True)
#     username = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     phone = models.CharField(max_length=15)
#     address = models.CharField(max_length=100)
#     pdf_file = models.FileField(upload_to='pdfs/')

#model for student
class Student(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    partner = models.BooleanField(default=False) 

    def __str__(self):
        return f"Student->{self.first_name}"


class Blank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class SubmittedName(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    