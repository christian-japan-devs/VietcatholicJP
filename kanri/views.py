from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (CommunitySerializer)
from .models import Community
from lib.error_messages import *
# Create your views here.

class CommunityListViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/community/getall/
    def getall(self, request):
        res = {
            'status': 'error',
            'communities': {},
            'message': ''
        }
        try:
            community = Community.objects.filter(is_active=True).order_by('name')
            if(community):
                serializer = CommunitySerializer(community, many=True)
                res['communities'] = serializer.data
            res['status'] = 'ok'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    # /api/community/<str:slug>/ for more detail.
    def retrieve(self, request, slug=None):
        res = {
            'status': 'error',
            'community': {},
            'sameRegionGroups':{},
            'message': ''
        }
        try:
            group = Community.objects.get(slug=slug)
            serializer = CommunitySerializer(group)
            res['status'] = 'ok'
            res['community'] = serializer.data
            communities = Community.objects.filter(is_active=True,region=group.region).exclude(id=group.id).order_by('-created_on')
            serializer1 = CommunitySerializer(communities, many=True)
            res['sameRegionGroups'] = serializer1.data
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            print(sys.exc_info())
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
class ContactViewSet(viewsets.ViewSet):
    
    permission_classes = (AllowAny,)
    # /api/contact-us/create
    def create(self, request):
        try:
            res = {
                'status': 'error',
                'message': 'Câu hỏi của bạn không được hệ thống chấp nhận.'
            }
            from .serializers import ContactUsSerializer
            serializer = ContactUsSerializer(data=request.data)
            #print(serializer.data)
            if serializer.is_valid():
                contact = serializer.save()
                contact.save()
                res['status'] = 'ok'
                res['message'] = 'Câu hỏi của bạn đã được gửi đi, vui lòng kiểm tra email trong vòng 24h.'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            print(sys.exc_info())
            res['message'] = SYSTEM_ERROR_0001
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContactUpdateViewSet(viewsets.ViewSet):    
    permission_classes = (IsAuthenticated,)
    # /api/contact-us/update/?cid=
    def update(self, request):  # /api/account/
        try:
            res = {
                'status': 'error',
                'message': 'Câu trả lời của bạn gửi đi không thành công.'
            }
            from .serializers import ContactUsSerializer
            from .models import ContactUs
            from .controller import reply_to_user_question
            id = request.GET.get('cid','')
            if id:
                contact_us = ContactUs.objects.get(id=id)
                if contact_us:
                    if not contact_us.is_replied:
                        serializer = ContactUsSerializer(contact_us,data=request.data, partial=True)
                        #print(serializer.data)
                        if serializer.is_valid():
                            contact_us_update = serializer.save()
                            if reply_to_user_question(contact_us_update):
                                contact_us_update.is_replied = True
                                contact_us_update.updated_user = request.user
                                contact_us_update.updated_on = timezone.now()
                                contact_us_update.save()
                                res['status'] = 'ok'
                                res['message'] = 'Câu trả lời đã được gửi đi thành công.'
                            else:
                                res['message'] = 'Câu trả lời của bạn gửi đi không thành công.'
                        else:
                            res['message'] = serializer.errors
                    else:
                        res['message'] = 'Câu hỏi đã được trả lời'
                else:
                    res['message'] = 'Câu hỏi không có trong hệ thống'
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            res['status'] = 'error'
            print(sys.exc_info())
            res['message'] = SYSTEM_ERROR_0001
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)