from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from .models import YoutubeVideo, Letter

class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('userId','saint_name','full_name','image')

class LetterShortSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer()
    class Meta:
        model = Letter
        fields = (
            'id', 'title', 'slug', 'imageUrl', 'excerpt', 'author','created_on'
        )

class LetterContentSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer()
    class Meta:
        model = Letter
        fields = (
            'id', 'title', 'slug', 'imageUrl', 'content', 'author','created_on'
        )