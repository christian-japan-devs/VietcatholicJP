from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import YoutubeVideo, Letter, MassDateSchedule, MassTimeSchedule, Announcement
from kanri.models import Father, Province, Church
from kanri.serializers import FatherContactSerializer, ChurchContactSerializer,ProvinceSerializer


class LetterShortSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Letter
        fields = (
            'id', 'title', 'slug', 'image_url', 'excerpt', 'author','created_on'
        )

class LetterContentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Letter
        fields = (
            'id', 'title', 'slug', 'image_url','excerpt','content', 'author','number_readed','number_shared','created_on'
        )

class LetterSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = (
            'id','title', 'slug'
        )

class MassDateScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MassDateSchedule
        fields = ('id','date','title','slug','gospel')

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

class AnnouncementShortSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Announcement
        fields = (
            'id', 'title', 'slug', 'image_url', 'excerpt', 'author','created_on'
        )

class AnnouncementContentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Announcement
        fields = (
            'id', 'title', 'slug', 'image_url','excerpt','content', 'author','created_on','number_shared','number_readed','google_map_link','register_link','event_date_time'
        )

class AnnouncementSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = (
            'id','title', 'slug'
        )

class YoutubeVideoSerializer(serializers.ModelSerializer):
    created_user = UserDetailSerializer()
    class Meta:
        model = YoutubeVideo
        fields = (
            'id', 'title', 'slug', 'youtube_url','excerpt','created_user'
        )