from django.contrib import admin
from .models import CustomUser, Book, Profile, ExamType, TestSchedules
from django import forms
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    ordering = ('username',)

# Register CustomUser with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Define the custom form for TestSchedule
class TestScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = TestSchedules
        fields = '__all__'
        
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'date_of_birth', 'address', 'student_id', 'course', 'batch', 'major', 'profile_image']
    search_fields = ['full_name', 'email', 'phone_number', 'student_id']

class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['test_type', 'test_model','city_name', 'location', 'current_fee', 'newest_fee']
    list_filter = ['test_type', 'test_model']
    search_fields = ['city_name', 'test_type','location']

admin.site.register(ExamType, ExamTypeAdmin)

# Define the admin class for TestSchedule
class TestScheduleAdmin(admin.ModelAdmin):
    form = TestScheduleAdminForm
    list_display = ('test_type', 'date', 'start_time', 'end_time', 'exam_type')
    list_filter = ('test_type', 'date', 'exam_type')
    search_fields = ('test_type', 'exam_type__city_name') 

# Register all models except TestSchedule
admin.site.register(Book)
admin.site.register(Profile,ProfileAdmin)

# Register TestSchedule using the custom admin class
admin.site.register(TestSchedules, TestScheduleAdmin)

