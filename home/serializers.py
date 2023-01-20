from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer
from .models import (YoutubeVideo,Aboutus, Letter, MassDateSchedule, MassTimeSchedule, 
                    Announcement, PostType, Post, PostContent, GospelRandom,
                    Gospel,GospelContent,GospelReflection,CommuintyPrayer, PrayerType,Prayer,CeremonyType,Ceremony)
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

class AboutusShortSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Aboutus
        fields = ('id', 'title','title_jp', 'slug', 'image_url', 'excerpt', 'author','created_on')

class AboutusContentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    class Meta:
        model = Aboutus
        fields = ('id', 'title','title_jp', 'slug', 'image_url','excerpt','content', 'author','created_on','number_shared','number_readed')


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

class GospelRandomShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = GospelRandom
        fields = ('id', 'word','word_jp','word_en','image_url','image_vertical','image_horizontal')

class GospelRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GospelRandom
        fields = ('id', 'word','image_url','image_vertical','image_horizontal','number_downloaded')

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

class PrayerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerType
        fields = ('id','name', 'name_jp','name_en')

class PrayerNoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prayer
        fields = ('id', 'name','name_jp', 'name_en','audio_link','audio_link_jp','audio_link_en','content','content_jp','content_en')

class PrayerTypePrayerSerializer(serializers.ModelSerializer):
    prayer_type_prayer = PrayerNoTypeSerializer(many=True, read_only=True)
    class Meta:
        model = PrayerType
        fields = ('id','name', 'name_jp','name_en','prayer_type_prayer')

class PrayerSlugSerializer(serializers.ModelSerializer):
    prayer_type = PrayerTypeSerializer()
    class Meta:
        model = Prayer
        fields = ('id','prayer_type','name','name_jp','name_en')

class PrayerSerializer(serializers.ModelSerializer):
    prayer_type = PrayerTypeSerializer()
    class Meta:
        model = Prayer
        fields = ('id','prayer_type', 'name','name_jp', 'name_en','audio_link','audio_link_jp','audio_link_en','content','content_jp','content_en')

class CommuintyPrayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuintyPrayer
        fields = ('id', 'title', 'slug', 'content','reference_link','created_on')


class CeremonyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeremonyType
        fields = ('id','name', 'name_jp','name_en')

class CeremonyNoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceremony
        fields = ('id', 'name','name_jp', 'name_en','audio_link','audio_link_jp','audio_link_en','content','content_jp','content_en')

class CeremonyTypePrayerSerializer(serializers.ModelSerializer):
    ceremonies = CeremonyNoTypeSerializer(many=True, read_only=True)
    class Meta:
        model = CeremonyType
        fields = ('id','name', 'name_jp','name_en','ceremonies')

class CeremonySlugSerializer(serializers.ModelSerializer):
    type = CeremonyTypeSerializer()
    class Meta:
        model = Ceremony
        fields = ('id','type','name','name_jp','name_en')
