from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UsernameField
import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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