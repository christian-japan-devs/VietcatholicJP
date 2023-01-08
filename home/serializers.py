from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import YoutubeVideo, Letter, MassDateSchedule, MassTimeSchedule
from kanri.models import Father, Province, Church
from kanri.serializers import FatherContactSerializer, ChurchContactSerializer,ProvinceSerializer


class LetterShortSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Letter
        fields = (
            'id', 'title', 'slug', 'imageUrl', 'excerpt', 'author','created_on'
        )

class LetterContentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Letter
        fields = (
            'id', 'title', 'slug', 'imageUrl','excerpt','content', 'author','created_on'
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