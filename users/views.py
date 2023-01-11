import sys, os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings

from .models import CustomUserModel
from rest_framework.authtoken.models import Token
from .serializers import (
    CustomUserSerializer
)

class GoogleLoginView(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get("FRONTEND_URL","http://localhost:3000/gio-le")
    client_class = OAuth2Client

# Create your views here.
class UserCreate(viewsets.ViewSet):
    
    permission_classes = (AllowAny,)
    def create(self, request):  # /api/account/
        print("Start create new account")
        try:
            serializer = CustomUserSerializer(data=request.data)
            #print(serializer.data)
            if serializer.is_valid():
                user = serializer.save()
                user.save()
                print(f'{user.email} was used to create new user.')
                token, created = Token.objects.get_or_create(user=user)
                res = {
                    'status': 'ok',
                    'data': {
                        'token': token.key,
                        'user_id': user.userId,
                        'confirm': 0,
                        'email': user.email
                    },
                    'message':''
                }
                from .controller import welcomeNewUser
                if(welcomeNewUser(user)):
                    res['status'] = 'ok'
                    res['message'] = 'Vui lòng kiểm tra hộp thư email để xác nhận tài khoản'
                    print(f'sened email to new user by {user.email}')
                else:
                    res['status'] = 'error'
                    res['message'] = f'Tài khoản đã được tạo, nhưng không thể gửi email tới {user.email} đã đăng ký.'
                    print(f'Tài khoản đã được tạo, nhưng không thể gửi email tới {user.email} đã đăng ký.')
                if(res['status']=='ok'):
                    return Response(res, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                res = {
                    'status': 'error',
                    'message': serializer.errors
                }
                #print(request.data)
                print('End request create new account error')
                print(serializer.errors)
                return Response(res, status=status.HTTP_226_IM_USED)
        except:
            #print(request.data)
            print(f"Create new user error: {sys.exc_info()[0]}")
            res = {
                    'status': 'error',
                    'message': {'system':'Không thể tạo tài khoản. Vui lòng liên hệ quản trị hệ thống.',
                                'error':{sys.exc_info()[0]}
                                }
                }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def requestPassword(self, request):
        res = {
            'status': 'error',
            'data': {
                'token': '',
                'user_id': '',
                'email': ''
            },
            'message': ''
        }
        try:
            req_email = request.data.get('email', '')
            if not CustomUserModel.objects.filter(email=req_email).exists():
                    res['status'] = 'error'
                    res['message'] = f'Email {req_email} này chưa được đăng ký, xin vui lòng kiểm tra lại.'
                    print(f"{req_email} not exists for reset password request.")
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUserModel.objects.get(email=req_email)
            if user:
                from .controller import userRequestResetPass
                print(user.username)
                if(userRequestResetPass(user, user.username, req_email)):
                    res['status'] = 'ok'
                    res['message'] = 'Vui lòng kiểm tra hộp thư đến trong email của bạn để đổi mật khẩu.'
                    return Response(res, status=status.HTTP_200_OK)
            res['status'] = ERROR
            res['message'] = 'Email này chưa được đăng ký, xin vui lòng kiểm tra lại'
            return Response(res, status=status.HTTP_200_OK)
        except:
            print("End request reset password error: ", sys.exc_info()[0])
            res['status'] = ERROR
            res['message'] = SYSTEM_QUERY_0001
            return Response(res, status=status.HTTP_200_OK)

    def resetPassword(self, request):  #
        res = {
            'status': 'error',
            'data': {
                'token': '',
                'username': '',
                'email': ''
            },
            'message': ''
        }
        try:
            # If authenticated user request reset password.
            if(request.auth):
                auth_user = request.user
                old_password = request.data.get('oldPassword', '')
                new_password = request.data.get('newPassword', '')
                if(auth_user.check_password(old_password)):
                    auth_user.set_password(new_password)
                    auth_user.save()
                    # Remove security code
                    userprofile = auth_user.userprofile
                    userprofile.profile_code = ''
                    userprofile.save()
                    token, created = Token.objects.get_or_create(
                        user=auth_user)
                    res['status'] = 'ok'
                    res['data']['token'] = token.key
                    res['message'] = 'Đổi mật khẩu thành công'
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    res['status'] = ERROR
                    res['message'] = 'Mật khẩu cũ không đúng.'
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Else Unauthenticated user request for reseting password from email.
                req_uid = request.data.get('uid', '')
                req_pass = request.data.get('password', '')
                re_code = request.data.get('code', '')
                if not CustomUserModel.objects.filter(userId=req_uid).exists():
                    res['status'] = 'error'
                    res['message'] = 'Tài khoản này không tồn tại.'
                    print(f"{req_uid} not exists for password chage.")
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                #TODO: check password reset time limit 30 minutes from last updated time.
                user = CustomUserModel.objects.get(userId=req_uid)
                if user:
                    userprofile = user.profile
                    if(userprofile.profile_code == re_code):
                        user.set_password(req_pass)
                        user.save()
                        # Remove security code
                        userprofile.profile_code = ''
                        userprofile.save()
                        res['status'] = 'ok'
                        res['data']['username'] = user.username
                        res['data']['email'] = user.email
                        res['message'] = 'Đổi mật khẩu thành công'
                        return Response(res, status=status.HTTP_200_OK)
                    else:
                        res['status'] = ERROR
                        res['message'] = 'Mã bảo mật không hợp lệ.'
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)
                else:
                    res['status'] = ERROR
                    res['message'] = 'Tài khoản không hợp lệ.'
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except:
            print("End reset password error: ", sys.exc_info()[0])
            res['status'] = ERROR
            res['message'] = sys.exc_info()
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    # confirm request api
    def confirm(self, request):  # /api/account/confirm
        res = {
            'status': 'error',
            'data': {
                'token': '',
                'username': '',
                'confirm': '',
                'redirect': ''
            },
            'message': ''
        }
        try:
            req_uid = request.data.get('uid', '')
            re_code = request.data.get('code', '')
            if not CustomUserModel.objects.filter(userId=req_uid).exists():
                res['status'] = 'warm'
                res['message'] = 'Tài khoản này không tồn tại.'
                print(f"{req_uid} not exists for conrfirm request.")
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUserModel.objects.get(userId=req_uid)
            if user:
                userprofile = user.profile
                if(userprofile.profile_account_confimred):
                    res['status'] = 'ok'
                    res['data']['username'] = user.username
                    res['message'] = 'Tài khoản này đã được xác nhận.'
                    return Response(res, status=status.HTTP_202_ACCEPTED)
                if(userprofile.profile_code == re_code):
                    # Remove security code
                    userprofile.profile_code = ''
                    userprofile.profile_account_confimred = True
                    userprofile.save()
                    token, created = Token.objects.get_or_create(user=user)
                    res['status'] = 'ok'
                    res['data']['token'] = token.key
                    res['data']['username'] = user.username
                    res['data']['confirm'] = 1
                    res['data']['redirect'] = '/account/profile'
                    res['message'] = 'Xác nhận tài khoản thành công.'
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    res['status'] = 'warm'
                    res['message'] = 'Mã bảo mật không đúng'
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                res['status'] = 'warm'
                res['message'] = 'Tài khoản không đúng'
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except:
            print(f"{request.data.get('uid', '')} request confirm error: {sys.exc_info()[0]}")
            res['status'] = ERROR
            res['message'] = str(sys.exc_info())
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
