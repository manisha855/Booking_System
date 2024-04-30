from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, Booking, Profile, ExamType, Blank

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('User Does Not Exist')

            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')

        return super(UserLoginForm, self).clean(*args, **kwargs)
    
#register for individuals
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    role = forms.ChoiceField(label="Role", choices=[('individual', 'Individual'), ('partner', 'Partner')])

    class Meta:
        model = CustomUser  # Use your CustomUser model
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
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'passport', 'test_city', 'signature', 'signature_date', 'email', 'phone', 'test_model', 'delivery_method']

    

# class BookingForm(forms.ModelForm):
#     # city_name = forms.ModelChoiceField(queryset=ExamType.objects.values_list('city_name', flat=True).distinct())
    
#     class Meta:
#         model = Booking
#         fields = ['name', 'passport', 'test_city', 'signature', 'signature_date', 'email', 'phone', 'test_model', 'delivery_method']
#         widgets = {
#             'signature_date': forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-MM-dd'})
#         }

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         try:
#             validate_email(email)
#         except ValidationError:
#             raise forms.ValidationError("Please enter a valid email address.")
#         return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_image', 'email', 'phone_number', 'date_of_birth', 'address', 'student_id', 'course', 'batch', 'major'] 

class ExamForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['city_name', 'location', 'current_fee', 'newest_fee', 'test_type', 'test_model']   

#Demo
class BlankForm(forms.ModelForm):
    class Meta:
        model = Blank
        fields = ['name'] 