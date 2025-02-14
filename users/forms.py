from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import Group, Permission
import re
from tasks.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

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


class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass

# Added Extra fields with User Model
'''
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    bio = forms.CharField(required=False, widget=forms.Textarea(), label='Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)

        # Todo: handle error
        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)

        # Save UserProfile if available
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')

            if commit:
                self.userprofile.save()
        
        if commit:
            user.save()

        return user
'''

class EditProfileForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'profile_image']


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