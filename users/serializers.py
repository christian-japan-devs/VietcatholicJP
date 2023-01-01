from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUserModel
from django. contrib. auth. models import Group

"""
class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUserModel.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUserModel.objects.all())])

    class Meta:
        model = CustomUserModel
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user
"""

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = [
            'userId',
            'username',
            'email',
            'password',
        ]
    
    def create(self, validated_data):
        user = CustomUserModel.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        return user

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class CustomerSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = CustomUserModel
        fields = [
            'username',
            'email',
            'is_staff',
            'groups'
        ]
