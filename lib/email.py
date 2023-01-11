import sys
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from .constants import (FROM_EMAIL,CC_EMAIL,CODERANGE,APP_HOST_NAME,APP_FACEBOOK_LINK_1,APP_FACEBOOK_LINK_2)
from kanri.models import UserProfile

def send_email_to(to_user, subject, text_content, html_content):
    try:
        msg = EmailMultiAlternatives(
            subject, text_content, FROM_EMAIL, [to_user],cc=CC_EMAIL)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        print("Send email error: ", sys.exc_info()[0])

def RegisterInform(user):
    try:
        random_code = get_random_string(length=18, allowed_chars=CODERANGE)
        userprofile = UserProfile.objects.get(user=user)
        userprofile.code = random_code
        userprofile.code_created_time = timezone.now()
        userprofile.save()
        email = user.email
        user_name = user.full_name
        account_name = user.username
        user_id = user.userId
        time_now = timezone.now()
        random_title = str(time_now.date())+"-"+str(time_now.hour)+":"+str(time_now.minute) #get_random_string(length=4, allowed_chars=CODERANGE)
        subject = 'Vietcatholicjp, Đăng ký tham dự đại hội. '+str(random_title)
        # text content
        text_content = "Xin chào bạn "+ user_name +". bạn nhận được email này vì đã yêu cầu đặt lại mật khẩu cho tài khoản đăng nhập của bạn tại trang "+APP_HOST_NAME+". Xin nhấp vào đường dẫn phía dưới để cập nhật mật khẩu mới. Nếu không phải bạn xin vui lòng bỏ qua."
        text_content += APP_HOST_NAME+'/account/confirm/?uid='+str(user_id)+'&code='+random_code
        # html content
        html_content = '<h4>Xin chào '+ user_name +' !</h4><br>'
        # edit here main content
        html_content += '<p>Để hoàn thành việc đăng ký tham dự đại hội của bạn vui lòng làm theo các bước sau:</p>'
        html_content += '<p>Vui lòng xác nhận sau khi chuyển khoản thành công.</p>'
        html_content += '<br><div style="text-align:center;"><a href="'+APP_HOST_NAME+'/account/confirm/?uid='+str(user_id)+'&code='+random_code+'"><button style="background: #f54642;width: 50%;padding: 1rem 0rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Xác thực</button></a></div>'
        # footer
        html_content += '<br><p>Lưu ý email này được gửi tự động, xin vui lòng không liên lạc hoặc trả lời lại qua email này.</p>'
        html_content += '<p>Mọi thắc mắc xin gửi tin nhắn trực tiếp về một trong hai trang facebook sau: </p>'
        html_content += '<div style="display: inline;"><a href="'+APP_FACEBOOK_LINK_1+'"><button style="background: #008CBA;width: 40%;padding: 1rem 0.5rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Fb Giáo đoàn</button></a>'
        html_content += '<a href="'+APP_FACEBOOK_LINK_2+'"><button style="background: #008CBA;width: 40%;padding: 1rem 0.5rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;margin-left: 4px;">Fb Giới trẻ</button></a></div>'
        html_content += '<p>Hoặc gửi email về địa chỉ sau: '+CC_EMAIL[0]+' hoặc: '+CC_EMAIL[1]+'</p>'
        html_content += '<h4 style="color:#f54642;">Giáo đoàn công giáo Việt Nam tại Nhật. Chúc bạn một ngày an lành!<h4>'
        send_email_to(email, subject, text_content, html_content)
        return True
    except:
        print("RegisterInform error: ", sys.exc_info()[0])
        return False

def sendConfirmEmailToUser(user):
    try:
        random_code = get_random_string(length=18, allowed_chars=CODERANGE)
        random_title = get_random_string(length=4, allowed_chars=CODERANGE)
        userprofile = UserProfile.objects.get(user=user)
        userprofile.code = random_code
        userprofile.code_created_time = timezone.now()
        userprofile.save()
        email = user.email
        user_name = user.username
        subject = f'Vietcatholicjp, Xác nhận tài khoản.{random_title}'
        text_content = "Xin chào bạn "+ user_name +". bạn nhận được email này vì đã yêu cầu đặt lại mật khẩu cho tài khoản đăng nhập của bạn tại trang "+APP_HOST_NAME+". Xin nhấp vào đường dẫn phía dưới để cập nhật mật khẩu mới. Nếu không phải bạn xin vui lòng bỏ qua."
        text_content += ''+APP_HOST_NAME+'/account/confirm/?uid=' +user.userId+'&code='+random_code
        html_content = '<h5>Xin chào. '+ user_name +'<h5><br><p>Bạn nhận được email này vì đã dùng email này để tạo tài khoản tại trang '+APP_HOST_NAME+'.</p> <p>Xin nhấp vào nút xác thực phía dưới.</p><p>Nếu không phải bạn xin vui lòng bỏ qua.<p><p>Lưu ý email này được gửi tự động, xin vui lòng không liên lạc lại qua email này, mọi thắc mắc xin gửi tin nhắn trực tiếp về trang facebook của giáo đoàn công giáo Việt nam tại Nhật hoặc qua email: vietcatholicjp@gmail.com.</p><br><h5>Giáo đoàn công giáo Việt Nam tại Nhật. Chúc bạn một ngày an lành!<h5><br>'
        html_content += '<a href="'+APP_HOST_NAME+'/account/confirm/?uid='+user.userId+'&code='+random_code + \
            '"><button style="background: #f54642;width: 50%;padding: 1rem 0rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Xác thực</button></a>'
        send_email_to(email, subject, text_content, html_content)
        return True
    except:
        print("sendConfirmEmailToUser error: ", sys.exc_info()[0])
        return False