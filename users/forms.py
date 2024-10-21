from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms 


class CustomUserCreationForm(UserCreationForm):
    #form for creating a new user
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [ 'email', 'password1', 'password2']


class CustomUserChangeForm(UserCreationForm):
    #form for updating an existing user's email 
    class Meta:
        model = CustomUser
        fields = ("email",)

