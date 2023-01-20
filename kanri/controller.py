import sys
from django.utils import timezone
from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string

# Custom
from lib.constants import (CODERANGE,APP_HOST_NAME,CC_EMAIL,APP_FACEBOOK_LINK_1,APP_FACEBOOK_LINK_2,GOSPEL_RANDOM)
from lib.email import (send_email_to)

def reply_to_user_question(contact_us):
    try:
        email = contact_us.email
        name = contact_us.name
        #question = contact_us.question
        answer = contact_us.answer
        time_now = timezone.now()
        random_title = str(time_now.date())+"-"+str(time_now.hour)+":"+str(time_now.minute) #get_random_string(length=4, allowed_chars=CODERANGE)
        subject = 'Vietcatholicjp, liên lạc '+str(random_title)
        # text content
        text_content = "Xin chào bạn "+ name +". Bạn nhận được email này vì đã đặt câu hỏi tại trang "+APP_HOST_NAME+"."
        text_content += answer
        # html content
        html_content = '<h4>Xin chào '+ name +' !</h4><br><p>Liên quan đến nội dung câu hỏi mà bạn đặt cho chúng tôi, chúng tôi xin trả lời bạn như sau: </p><p>'
        html_content += answer
        html_content += '</p><br><p>Lưu ý email này được gửi tự động, xin vui lòng không liên lạc hoặc trả lời lại qua email này.</p>'
        html_content += '<p>Mọi thắc mắc xin gửi tin nhắn trực tiếp về một trong hai trang facebook sau: </p>'
        html_content += '<div style="display: inline;"><a href="'+APP_FACEBOOK_LINK_1+'"><button style="background: #008CBA;width: 40%;padding: 1rem 0.5rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;">Fb Giáo đoàn</button></a>'
        html_content += '<a href="'+APP_FACEBOOK_LINK_2+'"><button style="background: #008CBA;width: 40%;padding: 1rem 0.5rem;border: none; color: white;cursor: pointer;border-radius: 30px;font-weight: bolder;font-size: 1rem;margin-left: 4px;">Fb Giới trẻ</button></a></div>'
        html_content += '<p>Hoặc gửi email về địa chỉ sau: '+CC_EMAIL[0]+' hoặc: '+CC_EMAIL[1]+'</p>'
        html_content += '<h4 style="color:#f54642;">Giáo đoàn công giáo Việt Nam tại Nhật. Chúc bạn một ngày an lành!<h4>'
        send_email_to(email, subject, text_content, html_content)
        return True
    except:
        print("reply_to_user_question error: ", sys.exc_info()[0])
        return False

def updateAccessCount(page_name):
    from .models import AccessCount
    try:
        accessCount = AccessCount.objects.get(page=page_name,date=date.today())
    except AccessCount.DoesNotExist:
        accessCount = AccessCount(page=page_name,count=0)
    accessCount.count += 1
    accessCount.save()

def updateGospelCount(year):
    from .models import AccessCount
    try:
        accessCount = AccessCount.objects.get(page=GOSPEL_RANDOM,date__year=year)
    except AccessCount.DoesNotExist:
        accessCount = AccessCount(page=GOSPEL_RANDOM,count=0)
    accessCount.count += 1
    accessCount.save()