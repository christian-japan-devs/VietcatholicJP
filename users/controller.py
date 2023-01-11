
import sys
from django.utils import timezone
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from kanri.models import UserProfile
# Custom
from lib.constants import (CODERANGE,APP_HOST_NAME,CC_EMAIL,APP_FACEBOOK_LINK_1,APP_FACEBOOK_LINK_2)
from lib.email import (send_email_to)

def welcomeNewUser(user):
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
        subject = 'Vietcatholicjp, Xác nhận tài khoản. '+str(random_title)
        # text content
        text_content = "Xin chào bạn "+ user_name +". bạn nhận được email này vì đã yêu cầu đặt lại mật khẩu cho tài khoản đăng nhập của bạn tại trang "+APP_HOST_NAME+". Xin nhấp vào đường dẫn phía dưới để cập nhật mật khẩu mới. Nếu không phải bạn xin vui lòng bỏ qua."
        text_content += APP_HOST_NAME+'/account/confirm/?uid='+str(user_id)+'&code='+random_code
        # html content
        html_content = '<h4>Xin chào '+ user_name +' !</h4><br><p>Bạn nhận được email này vì đã dùng email này để tạo tài khoản <b>'+account_name+'</b> tại trang <i>'+APP_HOST_NAME+'</i>.</p><p>Xin nhấp vào nút xác thực phía dưới để xác nhận tài khoản thuộc về bạn.</p><p>Nếu không phải bạn xin vui lòng bỏ qua.<p>'
        html_content += '<br><div style="text-align:center;"><a href="'+APP_HOST_NAME+'/account/confirm/?uid='+str(user_id)+'&code='+random_code+'"><button style="background: #f54642;width: 50%;padding: 1rem 0rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Xác thực</button></a></div>'
        html_content += '<br><p>Lưu ý email này được gửi tự động, xin vui lòng không liên lạc hoặc trả lời lại qua email này.</p>'
        html_content += '<p>Mọi thắc mắc xin gửi tin nhắn trực tiếp về một trong hai trang facebook sau: </p>'
        html_content += '<div style="display: inline;"><a href="'+APP_FACEBOOK_LINK_1+'"><button style="background: #008CBA;width: 40%;padding: 1rem 0.5rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Fb Giáo đoàn</button></a>'
        html_content += '<a href="'+APP_FACEBOOK_LINK_2+'"><button style="background: #008CBA;width: 40%;padding: 1rem 0.5rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;margin-left: 4px;">Fb Giới trẻ</button></a></div>'
        html_content += '<p>Hoặc gửi email về địa chỉ sau: '+CC_EMAIL[0]+' hoặc: '+CC_EMAIL[1]+'</p>'
        html_content += '<h4 style="color:#f54642;">Giáo đoàn công giáo Việt Nam tại Nhật. Chúc bạn một ngày an lành!<h4>'
        send_email_to(email, subject, text_content, html_content)
        return True
    except:
        print("welcomeNewUser error: ", sys.exc_info()[0])
        return False