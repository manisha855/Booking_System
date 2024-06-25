from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('partner', 'Partner')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    registered_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='registrations')
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# Add related_name to resolve the clash for groups and user_permissions
CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=32, blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=CustomUser)

# Exam Types set by admin
class ExamType(models.Model):
    test_type = models.CharField(max_length=20)
    test_mode = models.CharField(max_length=20)
    current_fee = models.IntegerField()
    newest_fee = models.IntegerField()
    city_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"ExamType - {self.test_type}, {self.test_mode}"

class ExamDate(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='exam_dates')
    test_date = models.DateField()
    test_time = models.TimeField()

    def __str__(self):
        return f"Date/Time: {self.test_date},{self.test_time} for {self.exam_type.test_type}"

# class BookExamType(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
#     exam_date = models.ForeignKey(ExamDate, on_delete=models.CASCADE)
#     booked_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Booking for {self.user} - {self.exam_type} on {self.exam_date}" 

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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    test_takers_first_language = models.CharField(max_length=100, blank=True, null=True)
    test_takers_country = models.CharField(max_length=100, blank=True, null=True)
    education_level = models.CharField(max_length=50, blank=True, null=True)
    occupation_sector = models.CharField(max_length=50, blank=True, null=True)
    occupation_level = models.CharField(max_length=50, blank=True, null=True)
    interest_in_ielts = models.CharField(max_length=50, blank=True, null=True)
    purpose = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    exam_date = models.ForeignKey(ExamDate, on_delete=models.CASCADE)

     # Additional fields from ExamType
    city_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    test_mode = models.CharField(max_length=20, blank=True, null=True)
    test_type = models.CharField(max_length=200, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    test_time = models.TimeField(blank=True, null=True)
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
            self.test_type = self.exam_type.test_type
            self.test_date = self.exam_date.test_date
            self.test_time = self.exam_date.test_time
        else:
            # Clear only the additional fields if no ExamType is selected
            self.city_name = None
            self.location = None
            self.test_mode = None
            self.test_type = None
            self.test_date = None
            self.test_time = None

        # Call full_clean to perform model validation
        self.full_clean()

        # Call super to save the model instance
        super().save(*args, **kwargs)
    
 # Transaction Model   
# class Transaction(models.Model):
#     pidx = models.CharField(max_length=255)
#     transaction_id = models.CharField(max_length=255)
#     tidx = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     mobile = models.CharField(max_length=20)
#     status = models.CharField(max_length=50)
#     purchase_order_id = models.CharField(max_length=255)
#     purchase_order_name = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"Transaction {self.transaction_id} - {self.status}"


class Transaction(models.Model):
    txn_id = models.CharField(max_length=20, unique=True)
    txn_date = models.DateField()
    txn_amt = models.IntegerField()
    reference_id = models.CharField(max_length=20)
    remarks = models.CharField(max_length=50)
    particulars = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='PENDING')
    
    def _str_(self):
        return f"Transaction ID: {self.txn_id}"
