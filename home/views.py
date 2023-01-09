from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import (LetterShortSerializer,LetterContentSerializer,LetterSlugSerializer,
    AnnouncementShortSerializer, AnnouncementContentSerializer, AnnouncementSlugSerializer,
    YoutubeVideoSerializer, PostSlugSerializer, PostSerializer, PostContentSerializer
)

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

# api
class LetterListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/letter/
    def getfirstletter(self, request):
        get_type = request.GET.get('type','home')
        if get_type == 'home':
            letter = Letter.objects.filter(is_active=True).order_by('-created_on').first()
            serializer = LetterContentSerializer(letter)
            return Response(serializer.data)
        elif get_type == 'slug':
            letter = Letter.objects.filter(is_active=True).order_by('-created_on')[:10]
            serializer = LetterSlugSerializer(letter, many=True)
            return Response(serializer.data)
        else:
            letter = Letter.objects.filter(is_active=True).order_by('-created_on')[:10]
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
            letter1 = Letter.objects.filter(is_active=True).exclude(id=letter.id).order_by('-created_on')[:10]
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
    def getannouncements(self, request):
        res = {
            'status': 'error',
            'letter': {},
            'recentlyPostedLetter':{},
            'message': ''
        }
        try:
            get_type = request.GET.get('type','index')
            if get_type == 'index':
                announcement = Announcement.objects.filter(from_date__lte=timezone.now(),to_date__gte=timezone.now(),is_active=True).order_by('-priority_choice','is_active','created_on').first()
                serializer = AnnouncementContentSerializer(announcement)
                res['status'] = 'ok'
                res['announcement'] = serializer.data
                announcements = Announcement.objects.filter(from_date__lte=timezone.now(),to_date__gte=timezone.now(),is_active=True).exclude(id=announcement.id).order_by('-priority_choice','is_active','created_on')[:10]
                serializer1 = AnnouncementShortSerializer(announcements, many=True)
                res['announcements'] = serializer1.data
                return Response(res, status=status.HTTP_202_ACCEPTED)
            elif get_type == 'slug':
                announcement = Announcement.objects.filter(from_date__lte=timezone.now(),to_date__gte=timezone.now(),is_active=True).order_by('-priority_choice','is_active','created_on')[:10]
                serializer = AnnouncementSlugSerializer(announcement, many=True)
                return Response(serializer.data)
            else: #short
                announcement = Announcement.objects.filter(is_active=True,from_date__lte=timezone.now(),to_date__gte=timezone.now()).order_by('-priority_choice','is_active','created_on')[:10]
                serializer = AnnouncementShortSerializer(announcement, many=True)
                return Response(serializer.data)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/announcement/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'announcement': {},
            'announcements':{},
            'message': ''
        }
        try:
            announcement = Announcement.objects.get(slug=slug)
            serializer = AnnouncementContentSerializer(announcement)
            res['status'] = 'ok'
            res['announcement'] = serializer.data
            letter1 = Announcement.objects.filter(from_date__lte=timezone.now(),to_date__gte=timezone.now(),is_active=True).exclude(id=announcement.id).order_by('-priority_choice','is_active','created_on')[:10]
            serializer1 = AnnouncementShortSerializer(letter1, many=True)
            res['announcements'] = serializer1.data
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoLinksListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/videolinks/
    def getVideoLinks(self, request):
        get_type = request.GET.get('type','first')
        if get_type == 'first':
            youtubelink = YoutubeVideo.objects.filter(is_active=True).order_by('-created_on').first()
            serializer = YoutubeVideoSerializer(youtubelink)
            return Response(serializer.data)
        else:
            youtubelinks = YoutubeVideo.objects.filter(is_active=True).order_by('-created_on')[:10]
            serializer = YoutubeVideoSerializer(youtubelinks, many=True)
            return Response(serializer.data)

class PostListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/post/gettype/
    def gettypes(self, request):
        res = {
            'status': 'error',
            'post_type': {},
            'message': ''
        }
        try:
            posttype = PostType.objects.filter(is_active=True).order_by('name')
            serializer = PostSlugSerializer(posttype, many=True)
            res['post_type'] = serializer.data
            res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/posts/?place=&type=
    def getposts(self, request):
        res = {
            'status': 'error',
            'post': {},
            'recent_posts': [],
            'message': ''
        }
        try:
            get_type = request.GET.get('type','home')
            get_post_type_slug = request.GET.get('post_type_slug','all')
            if get_type == 'home':
                if get_post_type_slug == 'all':
                    post = Post.objects.filter(is_active=True).order_by('-created_on').first()
                else:
                    post_type = PostType.objects.get(slug=get_post_type_slug)
                    post = Post.objects.filter(is_active=True,post_type=post_type).order_by('-created_on').first()
                if(post):
                    post_serializer = PostSerializer(post)
                    post_content = PostContent.objects.filter(post=post).order_by('sequence')
                    post_content_serializer = PostContentSerializer(post_content, many=True)
                    recent_post = Post.objects.filter(is_active=True).exclude(id=post.id).order_by('-created_on')[:10]
                    recent_post_serializer = PostSerializer(recent_post,many=True)
                    res['post'] = {
                        "post_meta":post_serializer.data,
                        "content":post_content_serializer.data
                    }
                    res['recent_posts'] = recent_post_serializer.data
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
            elif get_type == 'recent':
                recent_post = Post.objects.filter(is_active=True).order_by('-created_on')[1:11]
                recent_post_serializer = PostSerializer(recent_post,many=True)
                res['status'] = 'ok'
                res['recent_posts'] = recent_post_serializer.data
                return Response(res, status=status.HTTP_202_ACCEPTED)
            else:
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            letter1 = Letter.objects.filter(is_active=True).exclude(id=letter.id).order_by('-created_on')[:10]
            serializer1 = LetterShortSerializer(letter1, many=True)
            res['recentlyPostedLetter'] = serializer1.data
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)