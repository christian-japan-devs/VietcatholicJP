from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (LetterShortSerializer,LetterContentSerializer)

from django import forms
from .models import Letter
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

class MassScheduleViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/massschedule/?type=
    def get_nearest_mass_schedule(self, request):
        res = {
            'status': 'error',
            'notice': {},
            'message': ''
        }
        try:
            get_type = request.GET.get('type','home')
            from .models import MassDateSchedule, MassTimeSchedule
            from .serializers import MassDateScheduleSerializer
            mass_schedule = MassDateSchedule.objects.filter(date__gte=timezone.now()).order_by('date').first()
            if mass_schedule:
                mass_schedule_details = MassTimeSchedule.objects.filter(date_schedule=mass_schedule).order_by('time')
                serializer = MassDateScheduleSerializer(mass_schedule_details, many=True)
                res['status'] = 'ok'
                res['mass_schedules'] = {
                    "title": mass_schedule.title,
                    "date": mass_schedule.date,
                    "time_schedule":serializer.data
                }
            else:
                res['status'] = 'ok'
                res['mass_schedules'] = {
                }
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)