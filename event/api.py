import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from lib.error_messages import (SYSTEM_ERROR_0001)

class EventViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    # /api/event/?is_active=1
    def get_available_event(self, request):
        res = {
            'status': 'error',
            'events': [],
            'message': ''
        }
        try:
            from .models import Event
            from .serializers import EventSerializer
            events = Event.objects.filter(event_date__gte=timezone.now(),is_active=True).order_by('-event_date')
            if events:
                serializer = EventSerializer(events, many=True)
                if serializer:
                    res['status'] = 'ok'
                    res['events'] = serializer.data
                    return Response(res, status=status.HTTP_202_ACCEPTED)
                else:
                    res['status'] = 'warning'
                    res['message'] = serializer.error
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # /api/event/get_program/?eid=
    def get_event_program(self, request):
        res = {
            'status': 'error',
            'event':{
                'event_meta':{},
                'event_programs': [],
            },
            'message': ''
        }
        try:
            eid = request.GET('eid','')
            from .models import Event, EventProgramDetail
            from .serializers import EventSerializer,EventProgramDetailSerializer
            event = Event.objects.get(id=eid)
            if event:
                event_programs = EventProgramDetail.objects.filter(event=event,is_active=True).order_by('-event_date','from_time')
                program_serializer = EventProgramDetailSerializer(event_programs, many=True)
                if program_serializer:
                    event_serializer = EventSerializer(event)
                    res['status'] = 'ok'
                    res['event']['event_meta'] = event_serializer.data
                    res['event']['event_programs'] = program_serializer.data
                    return Response(res, status=status.HTTP_202_ACCEPTED)
                else:
                    res['status'] = 'warning'
                    res['message'] = program_serializer.error
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['status'] = 'error'
            res['message'] = SYSTEM_ERROR_0001
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)