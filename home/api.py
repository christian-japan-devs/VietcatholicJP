from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from kanri.controller import updateAccessCount,updateGospelCount
from lib.constants import (POST_READING,LETTER_READING,GOSPEL_LISTENING
        ,GOSPEL_READING,PRAYER_READING,HOME_PAGE,MASS_SCHEDULE,GOSPEL_RANDOM)

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
            updateAccessCount(HOME_PAGE)
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
            from .models import MassDateSchedule
            from .serializers import MassDateFullScheduleSerializer
            get_type = request.GET.get('type','index')
            mass_schedules = MassDateSchedule.objects.filter(date__gte=timezone.now()).order_by('date')[:20]
            if mass_schedules:
                res['status'] = 'ok'
                if get_type == 'home':
                    serializer = MassDateFullScheduleSerializer(mass_schedules[0])
                    res['mass_schedules'] = [serializer.data,]
                else:
                    serializer = MassDateFullScheduleSerializer(mass_schedules, many=True)
                    res['mass_schedules'] = serializer.data
                    updateAccessCount(MASS_SCHEDULE)

            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/massschedule/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'mass_schedule': {},
            'message': ''
        }
        try:
            from .models import MassDateSchedule
            from .serializers import MassDateFullScheduleSerializer
            try:
                mass_schedule = MassDateSchedule.objects.get(slug=slug)
            except MassDateSchedule.DoesNotExist:
                mass_schedule = None
            if mass_schedule:
                serializer = MassDateFullScheduleSerializer(mass_schedule)
                res['mass_schedule'] = serializer.data
                res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AboutusViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/about-us/?type=
    def get_about_us(self, request):
        res = {
            'status': 'error',
            'about_us': {},
            'message': ''
        }
        try:
            from .models import Aboutus
            from .serializers import AboutusContentSerializer
            get_type = request.GET.get('type','index')
            if get_type == 'index':
                about_us = Aboutus.objects.filter(is_active=True, type='community').first()
                print(about_us)
                if about_us:
                    serializer = AboutusContentSerializer(about_us)
                    res['about_us'] = serializer.data
                    res['status'] = 'ok'
            else:
                about_uses = Aboutus.objects.filter(is_active=True).order_by('created_on')
                if about_uses:
                    serializer = AboutusContentSerializer(about_us,many=True)
                    res['about_us'] = serializer.data
                    res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/about-us/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'about_us': {},
            'message': ''
        }
        try:
            from .models import Aboutus
            from .serializers import AboutusContentSerializer
            try:
                about_us = Aboutus.objects.get(slug=slug)
            except Aboutus.DoesNotExist:
                about_us = None
            if about_us:
                serializer = AboutusContentSerializer(about_us)
                res['about_us'] = serializer.data
                res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GospelRandomViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/gospel-random/?type=
    def get_gospel_random(self, request):
        res = {
            'status': 'error',
            'gospel_random': {},
            'message': ''
        }
        try:
            from .models import GospelRandom
            from .serializers import GospelRandomShortSerializer,GospelRandomSerializer
            from random import randrange
            get_type = request.GET.get('type','home')
            if get_type == 'home':
                try:
                    random_id = randrange(100)+1
                    res['random_id'] = random_id
                    gospel_random = GospelRandom.objects.get(id=random_id)
                except GospelRandom.DoesNotExist:
                    gospel_random = None
                if gospel_random:
                    gospel_random.number_downloaded += 1
                    gospel_random.save()
                    serializer = GospelRandomShortSerializer(gospel_random)
                    res['gospel_random'] = serializer.data
                    res['status'] = 'ok'
                    updateGospelCount(2023)
            else:
                try:
                    random_id = randrange(100)+1
                    gospel_random = GospelRandom.objects.get(id=random_id)
                except GospelRandom.DoesNotExist:
                    gospel_random = None
                if gospel_random:
                    gospel_random.number_downloaded += 1
                    gospel_random.save()
                    serializer = GospelRandomSerializer(gospel_random)
                    res['gospel_random'] = serializer.data
                    res['status'] = 'ok'
                    updateGospelCount(2023)
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#TODO: copy this sample viewset to create new api
class SampleViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/massschedule/?type=
    def get_(self, request):
        res = {
            'status': 'error',
            'mass_schedules': {},
            'message': ''
        }
        try:
            from .models import MassDateSchedule
            from .serializers import MassDateFullScheduleSerializer
            get_type = request.GET.get('type','home')
            if get_type == 'home':
                pass
            else:
                pass
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/massschedule/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'mass_schedule': {},
            'message': ''
        }
        try:
            from .models import MassDateSchedule
            from .serializers import MassDateFullScheduleSerializer
            try:
                mass_schedule = MassDateSchedule.objects.get(slug=slug)
            except MassDateSchedule.DoesNotExist:
                mass_schedule = None
            if mass_schedule:
                serializer = MassDateFullScheduleSerializer(mass_schedule)
                res['mass_schedule'] = serializer.data
                res['status'] = 'ok'
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
            get_post_type_slug = request.GET.get('post_type','all')
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
                    if get_post_type_slug == 'all':
                        recent_post = Post.objects.filter(is_active=True).exclude(id=post.id).order_by('-created_on')[:10]
                    else:
                        recent_post = Post.objects.filter(is_active=True,post_type=post_type).exclude(id=post.id).order_by('-created_on')[:10]
                    recent_post_serializer = PostSerializer(recent_post,many=True)
                    res['post']['meta_data'] = post_serializer.data
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

class PrayerViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/prayer/?where=
    def get_prayer(self, request):
        res = {
            'status': 'error',
            'prayers': {},
            'prayer_types':{},
            'message': ''
        }
        try:
            from .models import PrayerType,Prayer
            from .serializers import PrayerSerializer,PrayerSlugSerializer,PrayerSlugSerializer,PrayerTypePrayerSerializer
            get_where = request.GET.get('where','index')
            get_type = request.GET.get('type','')
            if get_type == '':
                if get_where == 'index':
                    prayer_types = PrayerType.objects.filter(is_active=True).order_by('-created_on')
                    if prayer_types:
                        prayer_serializer = PrayerTypePrayerSerializer(prayer_types, many = True)
                        res['prayer_types'] = prayer_serializer.data
                else:
                    prayers = Prayer.objects.filter(is_active=True).order_by('-created_on')
                    prayer_serializer = PrayerSlugSerializer(prayers, many = True)
                    res['prayers'] = prayer_serializer.data
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
            else:
                try:
                    prayer_type = PrayerType.objects.get(id=int(get_type))
                    #prayers = Prayer.objects.filter(is_active=True,prayer_type=prayer_type).order_by('-created_on')
                    prayer_serializer = PrayerTypePrayerSerializer(prayer_type)
                    res['prayer_types'] = prayer_serializer.data
                    res['status'] = 'ok'
                    return Response(res, status=status.HTTP_202_ACCEPTED)
                except PrayerType.DoesNotExist:
                    return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/prayer/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'prayer': {},
            'message': ''
        }
        try:
            from .models import Prayer
            from .serializers import PrayerSerializer
            try:
                prayer = Prayer.objects.get(slug=slug)
            except Prayer.DoesNotExist:
                prayer = None
            if prayer:
                serializer = PrayerSerializer(prayer)
                res['prayer'] = serializer.data
                res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PrayerTypeViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/prayer-type/?where=
    def get_prayer(self, request):
        res = {
            'status': 'error',
            'prayer_types':{},
            'message': ''
        }
        try:
            from .models import PrayerType
            from .serializers import PrayerTypeSerializer
            get_where = request.GET.get('where','index')
            if get_where == 'index':
                prayer_types = PrayerType.objects.filter(is_active=True).order_by('name')
                prayer_types_serializer = PrayerTypeSerializer(prayer_types, many = True)
                res['prayer_types'] = prayer_types_serializer.data
                res['status'] = 'ok'
            else:
                pass
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CeremonyViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/ceremony/?where=
    def get_prayer(self, request):
        res = {
            'status': 'error',
            'ceremonies': {},
            'ceremony_types':{},
            'message': ''
        }
        try:
            from .models import CeremonyType,Ceremony
            from .serializers import CeremonyTypePrayerSerializer,CeremonySlugSerializer
            get_where = request.GET.get('where','index')
            get_type = request.GET.get('type','')
            if get_type == '':
                if get_where == 'index':
                    ceremony_types = CeremonyType.objects.filter(is_active=True).order_by('-created_on')
                    if ceremony_types:
                        ceremony_serializer = CeremonyTypePrayerSerializer(ceremony_types, many = True)
                        res['ceremony_types'] = ceremony_serializer.data
                else:
                    ceremonies = Ceremony.objects.filter(is_active=True).order_by('-created_on')
                    ceremony_serializer = CeremonySlugSerializer(ceremonies, many = True)
                    res['ceremonies'] = ceremony_serializer.data
                res['status'] = 'ok'
                return Response(res, status=status.HTTP_202_ACCEPTED)
            else:
                try:
                    ceremony_type = CeremonyType.objects.get(id=int(get_type))
                    #prayers = Prayer.objects.filter(is_active=True,prayer_type=prayer_type).order_by('-created_on')
                    ceremony_serializer = CeremonyTypePrayerSerializer(ceremony_type)
                    res['ceremony_types'] = ceremony_serializer.data
                    res['status'] = 'ok'
                    return Response(res, status=status.HTTP_202_ACCEPTED)
                except CeremonyType.DoesNotExist:
                    return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/ceremony/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'ceremony': {},
            'message': ''
        }
        try:
            from .models import Ceremony
            from .serializers import CeremonyNoTypeSerializer
            try:
                ceremony = Ceremony.objects.get(slug=slug)
            except Ceremony.DoesNotExist:
                ceremony = None
            if ceremony:
                serializer = CeremonyNoTypeSerializer(ceremony)
                res['ceremony'] = serializer.data
                res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)