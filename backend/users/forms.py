from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class TeacherProfile(forms.ModelForm):
    class Meta:
        model = teacher_profile
        fields = ['university_picture','university_name','position','bio']
        
class CompanyProfile(forms.ModelForm):
    class Meta:
        model = recruiter_profile
        fields = ['logo','company_name','address','mobile_number']