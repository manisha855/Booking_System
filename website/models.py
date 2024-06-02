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

#Exam Tyes set by admin
class ExamType(models.Model):
    city_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    current_fee = models.IntegerField()
    newest_fee = models.IntegerField()
    test_type = models.CharField(max_length=20)  
    test_model = models.CharField(max_length=20)  

    def __str__(self):
        return f"{self.city_name} ExamType - {self.test_type}"
    
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
        return ExamType.objects.values_list('test_type', flat=True).distinct()    
    
#Model for booking
class Book(models.Model):
    name = models.CharField(max_length=100)
    passport = models.CharField(max_length=100)
    test_city = models.CharField(max_length=100, blank=True)
    passportfile = models.FileField(upload_to='pdf_files/')  # FileField for passport
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    exam_type = models.ForeignKey('ExamType', on_delete=models.CASCADE)
    test_schedule = models.ForeignKey('TestSchedules', on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking - {self.name}" 
    
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
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile -> {self.full_name}"
    
class Transaction(models.Model):
    pidx = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    tidx = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile = models.CharField(max_length=20)
    status = models.CharField(max_length=50)
    purchase_order_id = models.CharField(max_length=255)
    purchase_order_name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"    
