from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'input input-bordered','type':'text', 'placeholder': 'username', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input input-bordered',
            'type':'password',
            'placeholder': 'password',
            'id': 'password',
        }
))