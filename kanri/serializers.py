from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import Father, Province, Church, Region, Community

class FatherContactSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Father
        fields = ('id','user','region','province','address','facebook','phone_number')

class ChurchContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = ('id','name','phone','email','address','google_map_link')

class ChurchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = ('id','name','phone','email','address','google_map_link')

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id','kanji','name','nation')

class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = Province
        fields = ('id','kanji','name','region')

class CommunitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    church = ChurchContactSerializer()
    class Meta:
        model = Community
        fields = ('id','name','name_jp','image','type','introduction','url','province','church')
