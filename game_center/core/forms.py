from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Users
        fields = ["username", "email", "password1", "password2"]