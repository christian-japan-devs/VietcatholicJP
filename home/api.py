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

from .models import Letter,Announcement,YoutubeVideo
from lib.error_messages import *

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
            from .models import MassDateSchedule, MassTimeSchedule
            from .serializers import MassDateScheduleSerializer
            mass_schedule = MassDateSchedule.objects.filter(date__gte=timezone.now()).order_by('date').first()
            if mass_schedule:
                mass_schedule_details = MassTimeSchedule.objects.filter(date_schedule=mass_schedule).order_by('time')
                serializer = MassDateScheduleSerializer(mass_schedule_details, many=True)
                res['status'] = 'ok'
                res['mass_schedules'] = {
                    'title': mass_schedule.title,
                    'date': mass_schedule.date,
                    'audio_link': mass_schedule.gospel.audio_link, #TODO: chage to metadata
                    'time_schedule':serializer.data
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
            'post': {
                'meta_data':{},
                'content':{}
            },
            'recent_posts': [],
            'message': ''
        }
        try:
            from .models import PostType, Post, PostContent
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
                    res['post']['post_meta'] = post_serializer.data
                    res['post']['content'] = post_content_serializer.data
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
    
    # /api/post/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'post': {
                'meta_data':{},
                'content':{}
            },
            'related_posts':[],
            'message': ''
        }
        try:
            from .models import PostType, Post, PostContent
            from .serializers import PostSerializer, PostContentSerializer
            post = Post.objects.filter(slug=slug).first()
            if post:
                post_serializer = PostSerializer(post)
                post_content = PostContent.objects.filter(post=post).order_by('sequence')
                post_content_serializer = PostContentSerializer(post_content, many=True)
                post_type = PostType.objects.get(id=post.post_type.id)
                related_posts = Post.objects.filter(is_active=True,post_type=post_type).exclude(id=post.id).order_by('-created_on')[:10]
                related_post_serializer = PostSerializer(related_posts,many=True)
                res['post']['post_meta'] = post_serializer.data
                res['post']['content'] = post_content_serializer.data
                res['related_posts'] = related_post_serializer.data
            res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GospelListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/gospel/getthisweek/
    def get_this_week(self, request):
        res = {
            'status': 'error',
            'gospel': {
                'meta_data':{},
                'content':{}
            },
            'community_prayer':{},
            'reflection':{},
            'next':[],
            'message': ''
        }
        try:
            from .models import Gospel, GospelContent,GospelReflection, CommuintyPrayer
            from .serializers import GospelSerializer,GospelShortSerializer, GospelContentSerializer, GospelReflectionSerializer, CommuintyPrayerSerializer
            gospels = Gospel.objects.filter(date__gte=timezone.now()).order_by('date')
            if gospels:
                gospel_serializer = GospelSerializer(gospels[0])
                res['gospel']['meta_data'] = gospel_serializer.data
                gospels_serializer = GospelShortSerializer(gospels[1:],many=True)
                res['next'] = gospels_serializer.data
                gospel_content = GospelContent.objects.filter(gospel = gospels[0]).order_by('sequence')
                if gospel_content:
                    gospel_content_serializer = GospelContentSerializer(gospel_content, many = True)
                    res['gospel']['content'] = gospel_content_serializer.data
                community_prayer = CommuintyPrayer.objects.filter(gospel = gospels[0]).first()
                if community_prayer:
                    community_prayer_serializer = CommuintyPrayerSerializer(community_prayer)
                    res['community_prayer'] = community_prayer_serializer.data
                gospel_reflection = GospelReflection.objects.filter(gospel = gospels[0]).first()
                if gospel_reflection:
                    gospel_reflection_serializer = GospelReflectionSerializer(gospel_reflection)
                    res['reflection'] = gospel_reflection_serializer.data
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
            res['status'] = 'warning'
            res['message'] = 'no-data'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/gospel/?date=
    def get_by_date(self, request):
        res = {
            'status': 'error',
            'gospel': {
                'meta_data':{},
                'content':{}
            },
            'reflection':{},
            'next':[],
            'message': ''
        }
        try:
            from .models import Gospel, GospelContent,GospelReflection
            from .serializers import GospelSerializer,GospelShortSerializer, GospelContentSerializer, GospelReflectionSerializer
            get_date = request.GET.get('date','')
            if get_date != '':
                gospel = Gospel.objects.filter(date=get_date)
                if gospel:
                    res['gospel'] = GospelSerializer(gospel).data
                res['status'] = 'ok'
            else:
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/gospel/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'gospel': {
                'meta_data':{},
                'content':{}
            },
            'reflection':{},
            'next':[],
            'message': ''
        }
        try:
            from .models import Gospel, GospelContent,GospelReflection, CommuintyPrayer
            from .serializers import GospelSerializer,GospelShortSerializer, GospelContentSerializer, GospelReflectionSerializer,CommuintyPrayerSerializer
            gospel = Gospel.objects.get(slug=slug)
            gospels = Gospel.objects.filter(date__gte=timezone.now()).exclude(id=gospel.id).order_by('date')
            if gospel:
                gospel_serializer = GospelSerializer(gospel)
                res['gospel']['meta_data'] = gospel_serializer.data
                gospels_serializer = GospelShortSerializer(gospels,many=True)
                res['next'] = gospels_serializer.data
                gospel_content = GospelContent.objects.filter(gospel = gospel).order_by('sequence')
                if gospel_content:
                    gospel_content_serializer = GospelContentSerializer(gospel_content, many = True)
                    res['gospel']['content'] = gospel_content_serializer.data
                community_prayer = CommuintyPrayer.objects.filter(gospel = gospel).first()
                if community_prayer:
                    community_prayer_serializer = CommuintyPrayerSerializer(community_prayer)
                    res['community_prayer'] = community_prayer_serializer.data
                gospel_reflection = GospelReflection.objects.filter(gospel = gospel).first()
                if gospel_reflection:
                    gospel_reflection_serializer = GospelReflectionSerializer(gospel_reflection)
                    res['reflection'] = gospel_reflection_serializer.data
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
            res['status'] = 'warning'
            res['message'] = 'no-data'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)