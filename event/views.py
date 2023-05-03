import sys
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from lib.error_messages import *
from kanri.controller import updateAccessCount
# Create your views here.

class RegistrationListViewSet(viewsets.ViewSet):
    
    permission_classes = [AllowAny]
    # /api/community/
    def getall(self, request):
        res = {
            'status': 'error',
            'communities': {},
            'message': ''
        }
        try:
            from .models import RegistrationTemp
            from .serializers import RegistrationTempSerializer
            get_code = request.GET.get('code','none')
            payment_code = request.GET.get('pcode','none')
            get_email = request.GET.get('email','email')
            if payment_code != 'none':
                ticket = RegistrationTemp.objects.filter(status='OK',payment_code=payment_code,email=get_email).order_by('full_name')
                if(ticket):
                    tickets = RegistrationTemp.objects.filter(status='OK',payment_code=payment_code).order_by('full_name')
                    serializer = RegistrationTempSerializer(tickets, many=True)
                    res['tickets'] = serializer.data
                    res['status'] = 'ok'
                    updateAccessCount("Youth QR code")
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegistrationAdminViewSet(viewsets.ViewSet):    
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def create(self, request):  # /api/account/
        res = {
            'status': 'error',
            'communities': {},
            'message': ''
        }
        try:
            from .models import RegistrationTemp
            from .serializers import RegistrationTempFullSerializer
            serializer = RegistrationTempFullSerializer(data=request.data)
            #print(serializer.data)
            if serializer.is_valid():
                ticket = serializer.save()
                ticket.save()
                res = {
                    'status': 'ok',
                    'message':''
                }
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request):  # /api/account/
        res = {
            'status': 'error',
            'communities': {},
            'message': ''
        }
        try:
            from .models import RegistrationTemp
            from .serializers import RegistrationTempFullSerializer
            ticket_code = request.GET.get('code', '')
            email = request.GET.get('email', '')
            payment_status = request.GET.get('pstatus','')
            hardcode = request.data.get('hardcode', '')
            registrationTemp = RegistrationTemp.objects.get(email=email,ticket_code=ticket_code)
            if hardcode == 'admintration04292022':
                if registrationTemp:
                    registrationTemp.status = payment_status
                    registrationTemp.save()
                    res = {
                        'status': 'ok',
                        'message':''
                    }
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def checkin(self, request):  # /api/registration/checkin
        res = {
            'status': 'error',
            'message': ''
        }
        try:
            from .models import RegistrationTemp
            ticket_code = request.GET.get('code', '')
            email = request.GET.get('email', '')
            type = request.GET.get('type','checkin')
            present_status = request.GET.get('pstatus','')
            hardcode = request.GET.get('hardcode', '')
            registrationTemp = RegistrationTemp.objects.get(email=email,ticket_code=ticket_code)
            if hardcode == 'admintration04292022' and type == 'checkin':
                if registrationTemp.present_status == 'PS':
                    res = {
                        'status': 'presented',
                        'message': 'Mã này đã được duyệt!'
                    }
                elif registrationTemp.present_status == 'AB':
                    registrationTemp.present_status = 'PS'
                    registrationTemp.save()
                    res = {
                        'status': 'ok',
                        'message':'Check mã thành công!'
                    }
                else:
                    res = {
                        'status': 'error',
                        'message':'Bạn không thể duyệt ra vào.'
                    }
                    
            elif hardcode == 'admintration04292022' and type == 'inout':
                if registrationTemp.present_status == 'PS':
                    registrationTemp.present_status = 'GO'
                    registrationTemp.save()
                    res = {
                        'status': 'ok',
                        'message':'Check thành công, xin mời ra.'
                    }
                elif registrationTemp.present_status == 'GO':
                    registrationTemp.present_status = 'PS'
                    registrationTemp.save()
                    res = {
                        'status': 'ok',
                        'message':'Check thành công, xin mời vào!'
                    }
                else:
                   res = {
                        'status': 'error',
                        'message':'Bạn không check mã ra vào.'
                    } 
            return Response(res, status=status.HTTP_202_ACCEPTED)
        except:
            print(sys.exc_info())
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)