from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from django import forms
from .models import Letter,Announcement,YoutubeVideo,PostType, Post, PostContent
from lib.error_messages import *
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
