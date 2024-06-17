from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('partner', 'Partner')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# Add related_name to resolve the clash for groups and user_permissions
CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'

# Exam Types set by admin
class ExamType(models.Model):
    city_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    current_fee = models.IntegerField()
    newest_fee = models.IntegerField()
    test_type = models.CharField(max_length=20)  
    test_mode = models.CharField(max_length=20)  
    test_date = models.DateField()  
    test_time = models.TimeField()


    def __str__(self):
        return f"ExamType - {self.test_type}, City: {self.city_name}, Location: {self.location}, Test Date: {self.test_date}, Test Time: {self.test_time}"
    
# Model for booking
class Book(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    dob = models.DateField(verbose_name="Date of Birth")
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobileno = PhoneNumberField()
    country = models.CharField(max_length=100)
    address_line = models.CharField(max_length=255)
    town_or_city = models.CharField(max_length=100)
    passport_no = models.CharField(max_length=50)
    passport_expiry_date = models.DateField()
    passport_issuing_authority = models.CharField(max_length=100)
    passport_file = models.FileField(upload_to='passports/')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    test_takers_first_language = models.CharField(max_length=100)
    test_takers_country = models.CharField(max_length=100)
    education_level = models.CharField(max_length=50)
    occupation_sector = models.CharField(max_length=50)
    occupation_level = models.CharField(max_length=50)
    interest_in_ielts = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

     # Additional fields from ExamType
    city_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    test_mode = models.CharField(max_length=20, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    test_time = models.TimeField(blank=True, null=True)
    test_type = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.dob > timezone.now().date():
            raise ValidationError('Date of birth cannot be in the future.')

    def save(self, *args, **kwargs):
        if self.exam_type:
            # Fetch fields from ExamType if an ExamType is selected
            self.city_name = self.exam_type.city_name
            self.location = self.exam_type.location
            self.test_mode = self.exam_type.test_mode
            self.test_date = self.exam_type.test_date
            self.test_time = self.exam_type.test_time
            self.test_type = self.exam_type.test_type
        else:
            # Clear only the additional fields if no ExamType is selected
            self.city_name = None
            self.location = None
            self.test_mode = None
            self.test_date = None
            self.test_time = None
            self.test_type = None

        # Call full_clean to perform model validation
        self.full_clean()

        # Call super to save the model instance
        super().save(*args, **kwargs)

     
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
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
