from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError('Field must contain only letters')

def validate_letters_nums(value):
    if not value.isalnum():
        raise ValidationError('Field must contain letters and numbers')

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email',required=True, max_length=255)
    name = forms.CharField(label='Name' ,required=True, max_length=255,validators=[validate_letters_only])
    username=forms.CharField(label='Username',required=True,max_length=10,validators=[validate_letters_nums])
    password = forms.CharField(label='Password',required=True, min_length=8,widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Confirm Password',min_length=8,required=True, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username has already taken.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError(str(e))
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('password_confirmation')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data
