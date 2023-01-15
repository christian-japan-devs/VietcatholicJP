from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import (Father, Province, Church, Region, Community,
      RepresentativeResponsibility, Representative, RepresentativeAndCommunity,ContactUs)

class FatherContactSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Father
        fields = ('id','user','province','address','facebook','phone_number')

class RepresentativeContactSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Representative
        fields = ('id','user','province','address','facebook','phone_number',)

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
        fields = ('id','slug','name','name_jp','image','type','url','province','church')

class CommunityDetailSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    church = ChurchContactSerializer()
    class Meta:
        model = Community
        fields = ('id','slug','name','name_jp','image','type','introduction','url','province','church')

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('id','name','email','province','question','answer','is_replied')

    def create(self, validated_data):
        return ContactUs(**validated_data)

    def update(self, instance, validated_data):
        instance.answer = validated_data.get('answer', instance.answer)
        instance.save()
        return instance
