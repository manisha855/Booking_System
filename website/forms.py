from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm as DjangoPasswordResetForm, SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, Book, ExamType,ExamDate,ContactMessage
from django.utils import timezone

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError('User does not exist or incorrect password')

        return cleaned_data
    
#register for individuals
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    middle_name = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    role = forms.ChoiceField(label="Role", choices=[('student', 'Student'), ('partner', 'Partner')])

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.role = self.cleaned_data['role']
        user.middle_name = self.cleaned_data['middle_name']
        if commit:
            user.save()
        return user

#register student profile from admin and student portal    
class SignUpSubForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True, registered_by=None):
        user = super(SignUpSubForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set the password
        user.role = 'student'
        user.registered_by = registered_by
        if commit:
            user.save()
        return user  
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
#password reset form    
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

#exam form (setting of admin)        
class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = '__all__'  

class ExamDateForm(forms.ModelForm):
    class Meta:
        model = ExamDate
        fields = ['exam_type', 'test_date', 'test_time']    
     
# class BookTypeForm(forms.ModelForm):
#     exam_type = forms.ModelChoiceField(queryset=ExamType.objects.all())
#     exam_date = forms.ModelChoiceField(queryset=ExamDate.objects.all())

#     class Meta:
#         model = BookExamType
#         fields = ['exam_type', 'exam_date']

#Booking  done by admin, student & partners for students details  
class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set choices for gender field
        self.fields['gender'].widget.choices = Book.GENDER_CHOICES

        # Set default value for gender field
        if not self.instance.pk:  # Check if the instance (Book object) has not been saved yet
            self.initial['gender'] = 'F' 

    class Meta:
        model = Book
        fields = [
            'dob', 'name', 'email', 'mobileno', 'country', 'address_line',
            'town_or_city', 'passport_no', 'passport_expiry_date',
            'passport_issuing_authority', 'passport_file',
            'gender', 'test_takers_first_language', 'test_takers_country',
            'education_level','occupation_sector', 'occupation_level',
            'interest_in_ielts', 'purpose', 'exam_type', 'exam_date'
        ]

        widgets = {
            'gender': forms.RadioSelect,
        }
        # Remove default '---------'
        empty_label = None

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['exam_type'].queryset = ExamType.objects.all()

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob and dob > timezone.now().date():
            raise forms.ValidationError('Date of birth cannot be in the future.')
        return dob
    
# Mobile & email edit for student only
class MobileEmailForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['mobileno', 'email']