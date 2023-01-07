from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (LetterShortSerializer,LetterContentSerializer)

from django import forms
from .models import Letter
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

# api
class LetterListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/letter/
    def getfirstletter(self, request):
        get_type = request.GET.get('type','home')
        if get_type == 'home':
            letter = Letter.objects.filter(isActive=True).order_by('-created_on').first()
            serializer = LetterShortSerializer(letter)
            return Response(serializer.data)
        else:
            letter = Letter.objects.filter(isActive=True).order_by('-created_on')
            serializer = LetterShortSerializer(letter, many=True)
            return Response(serializer.data)
    
    # /api/letter/<str:slug> for more detail.
    def retrieve(self, request, slug=None):
        get_type = request.GET.get('type','slug')
        letter = Letter.objects.get(slug=slug)
        serializer = LetterContentSerializer(letter)
        return Response(serializer.data)