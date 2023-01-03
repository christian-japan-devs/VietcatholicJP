import sys
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from .constants import (FROM_EMAIL,CODERANGE,APP_HOST_NAME)
from users.models import Profile

def send_email_to(to_user, subject, text_content, html_content):
    try:
        msg = EmailMultiAlternatives(
            subject, text_content, FROM_EMAIL, [to_user])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        print("Send email error: ", sys.exc_info()[0])

def welcomeNewUser(user):
    try:
        random_code = get_random_string(length=18, allowed_chars=CODERANGE)
        random_title = get_random_string(length=4, allowed_chars=CODERANGE)
        if not Profile.objects.filter(profile_user = user).exists():
            Profile.objects.create(profile_user=user)

        userprofile = Profile.objects.get(profile_user=user)
        userprofile.profile_code = random_code
        userprofile.save()
        email = user.email
        user_name = user.username
        subject = f'Vietcatholicjp, Xác nhận tài khoản.{random_title}'
        text_content = "Xin chào bạn "+ user_name +". bạn nhận được email này vì đã yêu cầu đặt lại mật khẩu cho tài khoản đăng nhập của bạn tại trang "+APP_HOST_NAME+". Xin nhấp vào đường dẫn phía dưới để cập nhật mật khẩu mới. Nếu không phải bạn xin vui lòng bỏ qua."
        text_content += ''+APP_HOST_NAME+'/account/confirm/?uid=' +user.userId+'&code='+random_code
        html_content = '<h5>Xin chào. '+ user_name +'<h5><br><p>Bạn nhận được email này vì đã dùng email này để tạo tài khoản tại trang '+APP_HOST_NAME+'.</p> <p>Xin nhấp vào nút xác thực phía dưới.</p><p>Nếu không phải bạn xin vui lòng bỏ qua.<p><p>Lưu ý email này được gửi tự động, xin vui lòng không liên lạc hoặc trả lời lại qua email này, mọi thắc mắc xin gửi tin nhắn trực tiếp về trang facebook của giáo đoàn công giáo Việt nam tại Nhật hoặc qua email: vietcatholicjp@gmail.com.</p><br><h5>Giáo đoàn công giáo Việt Nam tại Nhật. Chúc bạn một ngày an lành!<h5><br>'
        html_content += '<a href="'+APP_HOST_NAME+'/account/confirm/?uid='+user.userId+'&code='+random_code + \
            '"><button style="background: #f54642;width: 50%;padding: 1rem 0rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Xác thực</button></a>'
        send_email_to(email, subject, text_content, html_content)
        return True
    except:
        print("welcomeNewUser error: ", sys.exc_info()[0])
        return False

def sendConfirmEmailToUser(user):
    try:
        random_code = get_random_string(length=18, allowed_chars=CODERANGE)
        random_title = get_random_string(length=4, allowed_chars=CODERANGE)
        if not Profile.objects.filter(user = user).exists():
            Profile.objects.create(user=user)
        userprofile = Profile.objects.get(user=user)
        userprofile.code = random_code
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