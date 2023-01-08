from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import (LetterShortSerializer,LetterContentSerializer,LetterSlugSerializer,
    AnnouncementShortSerializer, AnnouncementContentSerializer, AnnouncementSlugSerializer
)

from django import forms
from .models import Letter,Announcement
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
            serializer = LetterContentSerializer(letter)
            return Response(serializer.data)
        elif get_type == 'slug':
            letter = Letter.objects.filter(isActive=True).order_by('-created_on')[:10]
            serializer = LetterSlugSerializer(letter, many=True)
            return Response(serializer.data)
        else:
            letter = Letter.objects.filter(isActive=True).order_by('-created_on')[:10]
            serializer = LetterShortSerializer(letter, many=True)
            return Response(serializer.data)
    
    # /api/letter/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'letter': {},
            'recentlyPostedLetter':{},
            'message': ''
        }
        try:
            letter = Letter.objects.get(slug=slug)
            serializer = LetterContentSerializer(letter)
            res['status'] = 'ok'
            res['letter'] = serializer.data
            letter1 = Letter.objects.filter(isActive=True).exclude(id=letter.id).order_by('-created_on')[:10]
            serializer1 = LetterShortSerializer(letter1, many=True)
            res['recentlyPostedLetter'] = serializer1.data
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MassScheduleViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/massschedule/?type=
    def get_nearest_mass_schedule(self, request):
        res = {
            'status': 'error',
            'mass_schedules': {},
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

class AnnouncementListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/announcement/
    def getfirstletter(self, request):
        get_type = request.GET.get('type','home')
        if get_type == 'home':
            letter = Announcement.objects.filter(isActive=True).order_by('-created_on').first()
            serializer = AnnouncementContentSerializer(letter)
            return Response(serializer.data)
        elif get_type == 'slug':
            letter = Announcement.objects.filter(isActive=True).order_by('-created_on')[:10]
            serializer = AnnouncementSlugSerializer(letter, many=True)
            return Response(serializer.data)
        else:
            letter = Announcement.objects.filter(isActive=True).order_by('-created_on')[:10]
            serializer = AnnouncementShortSerializer(letter, many=True)
            return Response(serializer.data)
    
    # /api/announcement/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'letter': {},
            'recentlyPostedLetter':{},
            'message': ''
        }
        try:
            letter = Announcement.objects.get(slug=slug)
            serializer = AnnouncementContentSerializer(letter)
            res['status'] = 'ok'
            res['letter'] = serializer.data
            letter1 = Announcement.objects.filter(isActive=True).exclude(id=letter.id).order_by('-created_on')[:10]
            serializer1 = AnnouncementShortSerializer(letter1, many=True)
            res['recentlyPostedLetter'] = serializer1.data
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)