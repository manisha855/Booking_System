from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, Book, Profile, ExamType, TestSchedules

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
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    role = forms.ChoiceField(label="Role", choices=[('individual', 'Individual'), ('partner', 'Partner')])

    class Meta:
        model = CustomUser  
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

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
        if commit:
            user.save()
        return user 
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_image', 'email', 'phone_number', 'date_of_birth', 'address', 'student_id', 'course', 'batch', 'major'] 

class ExamForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['city_name', 'location', 'current_fee', 'newest_fee', 'test_type', 'test_model']

class TestSchedulesForm(forms.ModelForm):
    class Meta:
        model = TestSchedules
        fields = ['test_type', 'date', 'start_time', 'end_time', 'exam_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exam_type'].queryset = ExamType.objects.all()

#Booking    
class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['exam_type'].choices = self.get_exam_type_choices()

    def get_exam_type_choices(self):
        exam_types = ExamType.objects.all()
        choices = [(exam_type.id, f"{exam_type.test_type} - {exam_type.city_name}") for exam_type in exam_types]
        return choices
    
    class Meta:
        model = Book
        fields = ['name', 'passport', 'test_city', 'passportfile', 'email', 'phone', 'exam_type', 'test_schedule']
