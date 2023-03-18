from django.db import models
from rest_framework import serializers
from users.models import CustomUserModel
from users.serializers import UserDetailSerializer

from .models import (Event,EventProgramDetail,EventRuleContent,Registration,
            EventBoard,EventBoardAndMember,EventBoardTask,EventGroup,UserAndEventGroup,EventGroupScoreType,EventGroupScore,
            EventTransactionAccount,EventTransaction,RegistrationTemp)

class EventSerializer(serializers.ModelSerializer):
    created_user = UserDetailSerializer()
    class Meta:
        model = Event
        fields = ('id','title','slug','excerpt','image_url','event_date','from_time','to_time','address','google_map_link','number_of_ticket','created_on','created_user')

class EventDetailSerializer(serializers.ModelSerializer):
    created_user = UserDetailSerializer()
    class Meta:
        model = Event
        fields = ('id','title','slug','excerpt','image_url','event_date','from_time','to_time','number_of_ticket','event_fee','province','address','url','','google_map_link','created_on','created_user')

class EventProgramDetailSerializer(serializers.ModelSerializer):
    created_user = UserDetailSerializer()
    class Meta:
        model = EventProgramDetail
        fields = ('id','event','title','content','event_date','from_time','to_time','is_active','created_on','created_user')

class EventRuleContentSerializer(serializers.ModelSerializer):
    created_user = UserDetailSerializer()
    class Meta:
        model = EventRuleContent
        fields = ('id','event', 'title','sequence','image_url','chapter_summary','content','is_active','created_on','created_user')

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Registration
        fields = ('id','date_time', 'user')

class EventBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBoard
        fields = ('id','', '')

class EventBoardAndMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBoardAndMember
        fields = ('id','', '')

class EventBoardTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBoardTask
        fields = ('id','', '')

class EventGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGroup
        fields = ('id','', '')

class UserAndEventGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAndEventGroup
        fields = ('id','', '')

class EventGroupScoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGroupScoreType
        fields = ('id','', '')

class EventTransactionAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTransactionAccount
        fields = ('id','', '')

class EventTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTransaction
        fields = ('id','', '')


class RegistrationTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationTemp
        fields = ('id','status', 'payment_code','ticket_code','email','saint_name','full_name','birth_year','group_name','ticket','team_no')

class RegistrationTempFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationTemp
        fields = ('id','status', 'payment_code','ticket_code','email','saint_name','full_name','gender','birth_year','group_name','province','go_together','team_no','type','present_status')