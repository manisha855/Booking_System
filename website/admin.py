from django.contrib import admin
from .models import CustomUser, Book, ExamType
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
        
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'location', 'current_fee', 'newest_fee', 'test_type', 'test_mode']

admin.site.register(ExamType, ExamTypeAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'name', 'created_by')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name', 'created_by__username')
    ordering = ('-created_at',)

admin.site.register(Book, BookAdmin)