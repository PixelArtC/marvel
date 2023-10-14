from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    private_key = forms.CharField(required=False) 
    full_name = forms.CharField(max_length=100)  #  # Make sure it's not required

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email','full_name')
