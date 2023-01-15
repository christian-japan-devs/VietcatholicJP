from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import (YoutubeVideo, Letter, MassDateSchedule, MassTimeSchedule, 
                    Announcement, PostType, Post, PostContent,
                    Gospel,GospelContent,GospelReflection,CommuintyPrayer)
from kanri.models import Father, Province, Church
from kanri.serializers import FatherContactSerializer, ChurchContactSerializer,ProvinceSerializer


class LetterShortSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Letter
        fields = ('id', 'title', 'slug', 'image_url', 'excerpt', 'author','created_on','number_readed')

class LetterContentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Letter
        fields = ('id', 'title', 'slug', 'image_url','excerpt','content', 'author','number_readed','number_shared','created_on')

class LetterSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ('id','title', 'slug')

class MassDateSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = MassDateSchedule
        fields = ('id','date','title','slug','gospel')

class GospelLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gospel
        fields = ('id','title', 'slug','audio_link')

class MassDateTimeScheduleSerializer(serializers.ModelSerializer):
    father = FatherContactSerializer()
    church = ChurchContactSerializer()
    province = ProvinceSerializer()
    class Meta:
        model = MassTimeSchedule
        fields = ('id','time','father','church','province','notes')

class MassDateFullScheduleSerializer(serializers.ModelSerializer):
    gospel = GospelLinkSerializer()
    time_schedule = MassDateTimeScheduleSerializer(many=True, read_only=True)
    class Meta:
        model = MassDateSchedule
        fields = ('id','date','title','slug','gospel','time_schedule')

'''
class MassDateScheduleSerializer(serializers.ModelSerializer):
    father = FatherContactSerializer()
    church = ChurchContactSerializer()
    province = ProvinceSerializer()
    class Meta:
        model = MassTimeSchedule
        fields = ('id','time','father','church','province','notes')

class MassDateScheduleFullSerializer(serializers.ModelSerializer):
    date_schedule = MassDateScheduleSerializer()
    father = FatherContactSerializer()
    church = ChurchContactSerializer()
    province = ProvinceSerializer()
    class Meta:
        model = MassTimeSchedule
        fields = ('id','time','date_schedule','father','church','province','notes')
'''

class AnnouncementShortSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'slug', 'image_url', 'excerpt', 'author','created_on')

class AnnouncementContentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'slug', 'image_url','excerpt','content', 'author','created_on','number_shared','number_readed','google_map_link','register_link','event_date_time')

class AnnouncementSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id','title', 'slug')

class YoutubeVideoSerializer(serializers.ModelSerializer):
    created_user = UserDetailSerializer()
    class Meta:
        model = YoutubeVideo
        fields = ('id', 'title', 'slug', 'youtube_url','excerpt','created_user')

class PostSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = ('id','name', 'slug')

class PostSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug','audio_link', 'image_url', 'excerpt', 'author','created_on','number_readed','number_shared')

class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ('id', 'chapter_title', 'slug', 'image_url', 'content','chapter_summary')

class GospelSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gospel
        fields = ('id','title', 'slug')

class GospelShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gospel
        fields = ('id','title', 'slug','image_url', 'excerpt','date')

class GospelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gospel
        fields = ('id', 'title', 'slug','date','audio_link', 'image_url', 'excerpt','number_readed','number_shared')

class GospelContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GospelContent
        fields = ('id', 'chapter_title', 'slug', 'content','chapter_reference')

class GospelReflectionSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = GospelReflection
        fields = ('id', 'title', 'slug','audio_link','image_url', 'content','reference_link','author','number_readed','number_shared','created_on')

class CommuintyPrayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuintyPrayer
        fields = ('id', 'title', 'slug', 'content','reference_link','created_on')
