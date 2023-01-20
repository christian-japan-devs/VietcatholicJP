from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import (Father, Province, Church, Region, Community,
      RepresentativeResponsibility, Representative, RepresentativeAndCommunity,ContactUs)

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id','kanji','name','nation')

class ProvinceSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = Province
        fields = ('id','kanji','name','region')

class FatherContactSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Father
        fields = ('id','user','province','address','facebook','phone_number')

class FatherSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Father
        fields = ('id','user','province','address','facebook','phone_number')

class ProvinceFatherSerializer(serializers.ModelSerializer):
    father_province = FatherSerializer(many=True, read_only=True)
    class Meta:
        model = Province
        fields = ('id','kanji','name','father_province')

class RegionFatherSerializer(serializers.ModelSerializer):
    region_province = ProvinceFatherSerializer(many=True, read_only=True)
    class Meta:
        model = Region
        fields = ('id','kanji','name','region_province')

class RepresentativeContactSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Representative
        fields = ('id','user','province','address','facebook','phone_number',)

class ChurchContactSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    class Meta:
        model = Church
        fields = ('id','name','phone','email','province','address','google_map_link')

class ChurchDetailSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    class Meta:
        model = Church
        fields = ('id','name','kanji','image','url','phone','email','province','address','google_map_link')

class ProvinceChurchSerializer(serializers.ModelSerializer):
    church_province = ChurchDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Province
        fields = ('id','kanji','name','church_province')

class RegionChurchSerializer(serializers.ModelSerializer):
    region_province = ProvinceChurchSerializer(many=True, read_only=True)
    class Meta:
        model = Region
        fields = ('id','kanji','name','region_province')

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
