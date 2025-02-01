from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User, Group, Permission
import re
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        
        for field_text in ['username', 'password1', 'password2']:
            self.fields[field_text].help_text = None


class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError('This email already exists!! Try another.')
        
        return email

    def clean_password1(self): # field error
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 character!')
        if not (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[@#$%^&+=]', password)):
            errors.append('Your password must have at least 1 uppercase, 1 lowercase, 1 number and a special character.')

        if errors:
            raise forms.ValidationError(errors)
        
        return password
    
    def clean(self): # non field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password do not match!! Please correct it.')
        
        return cleaned_data
    

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
         queryset=Group.objects.all(),
         empty_label="Select a role"    
    )


class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset= Permission.objects.prefetch_related('content_type').all(),
        required= False,
        widget= forms.CheckboxSelectMultiple,
        label= 'Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']