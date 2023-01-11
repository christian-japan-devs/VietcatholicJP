from django.db import models
from django.utils import timezone

from tinymce.models import HTMLField
from users.models import CustomUserModel
from lib.constant_choices import (sequence_choise,event_status_choice
    ,membership_type,score_type,trasaction_type,task_statuses,priority_choice)
from lib.constants import (REGISTRED,NOT_PAIED,NOT_CONFIRM,ABSENT,NOT_YET)
from kanri.models import Province, Church, Father
from lib.help import compressImage

# Create your models here.
class Event(models.Model):
    title = models.CharField('Chủ đề',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    excerpt = models.TextField('Tóm tắt',null=True,blank=True,default='',help_text='Không quá 500 ký tự',max_length=500)
    image_url = models.ImageField('Hình ảnh',null=True,blank=True,upload_to='images/event')
    event_date = models.DateTimeField('Ngày',blank=True, null=True,auto_now_add = True)
    from_time= models.TimeField('Thời gian bắt đầu',blank=True, null=True, default=timezone.now)
    to_time= models.TimeField('Thời gian kết thúc',blank=True, null=True, default=timezone.now)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,related_name='event_province',on_delete=models.CASCADE)
    address = models.CharField('Địa chỉ hiện tại',default='',blank=True,max_length=300)
    google_map_link = models.CharField('googlemap link',max_length=500)
    event_fee = models.IntegerField('Phí tham dự',help_text='Phí tham dự , tiền yên',default=0)
    number_of_ticket = models.IntegerField('Số vé cho phép',help_text='Số vé cho phép',default=100)
    number_of_registered_ticket = models.IntegerField('Số vé đã đăng ký',default=0)
    number_of_confirmed_ticket = models.IntegerField('Số vé đã xác nhận',help_text='Số vé đã xác nhận sau khi đăng ký',default=0)
    url = models.CharField('Facebook link',help_text='Link facebook của sự kiện nếu có',null=True,blank=True,default='',max_length=200)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='event_created_user')
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ['event_date','-created_on','title']
        verbose_name = 'Sự kiện-0-sự kiện'
        verbose_name_plural = 'Sự kiện-0-sự kiện'

class EventProgramDetail(models.Model):
    event = models.ForeignKey(Event,verbose_name='Sự kiện',related_name='event_program_detail',on_delete=models.CASCADE)
    title = models.CharField('Tên chương trình',max_length=200)
    content = HTMLField('Nội dung chương trình')
    event_date = models.DateTimeField('Ngày',blank=True, null=True,auto_now_add = True)
    from_time= models.TimeField('Thời gian bắt đầu', default=timezone.now)
    to_time= models.TimeField('Thời gian kết thúc', default=timezone.now)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_detail_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_detail_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['event','event_date','-from_time','title']
        verbose_name = 'Sự kiện-1-chương trình'
        verbose_name_plural = 'Sự kiện-1-chương trình'


class EventRuleContent(models.Model):
    event = models.ForeignKey(Event,verbose_name='Sự kiện',related_name='event_rule_content',on_delete=models.CASCADE)
    title = models.CharField('Tên mục',max_length=200)
    slug = models.CharField('Slug',max_length=100)
    sequence = models.CharField('Thứ tự',default='0',choices=sequence_choise,max_length=4)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    chapter_summary = models.CharField('Tóm tắt',default='',null=True, blank=True,help_text='Không quá 500 ký tự',max_length=500)
    content = HTMLField('Nội dung')
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_rule_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_rule_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.rule_title

    class Meta:
        ordering = ['event','title','sequence','-created_on']
        verbose_name = 'Sự kiện-2-quy định'
        verbose_name_plural = 'Sự kiện-2-quy định'

class Registration(models.Model):
    date_time = models.DateTimeField('Ngày đăng ký',blank=True, null=True,auto_now = True)
    user = models.ForeignKey(CustomUserModel,verbose_name='Người đăng ký', on_delete=models.CASCADE,related_name='registration_user')
    event = models.ForeignKey(Event,verbose_name='Sự kiện', on_delete=models.CASCADE,related_name='registration_event')
    ticket_code = models.CharField('Mã vé',max_length=6,default='',null=True,blank=True)
    ticket_price = models.IntegerField('Giá vé',default=0,null=True,blank=True)
    registerd_status = models.CharField('Tình trạng đăng ký',max_length=4,default=REGISTRED,null=True,blank=True)
    payment_status = models.CharField('Tình trạng thanh toán',max_length=4,default=NOT_PAIED,null=True,blank=True)
    admin_confirm_status = models.CharField('Tình trạng admin xác nhận',max_length=4,choices=event_status_choice,default=NOT_CONFIRM,null=True,blank=True)
    attend_status = models.CharField('Tình trạng tham dự',max_length=4,choices=event_status_choice,default=ABSENT,null=True,blank=True)
    confirm_status = models.CharField('Tình trạng thanh toán xác nhận',max_length=3,choices=event_status_choice,default=NOT_CONFIRM,null=True,blank=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='registration_updated_user',default=None,blank=True,null=True)

    class Meta:
        ordering = ['event','-date_time','user']
        verbose_name = 'Sự kiện-4-đăng ký'
        verbose_name_plural = 'Sự kiện-3-đăng ký'

    def __str__(self):
        return f'{self.user.full_name}' #: {self.userseat}'

class EventBoard(models.Model):
    event = models.ForeignKey(Event,verbose_name='Sự kiện',related_name='event_board',on_delete=models.CASCADE)
    title = models.CharField('Tên Ban',max_length=200)
    slug = models.CharField('Slug',max_length=100)
    content = HTMLField('Nội dung công việc')
    facebook_link = models.TextField('Facebook group link',null=True,blank=True,default='',help_text='Link facebook',max_length=500)
    drive_link = models.TextField('Link drive',null=True,blank=True,default='',help_text='Link drive của Ban',max_length=500)
    is_active = models.BooleanField('Hoạt động',default=True, blank=True)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_board_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_board_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['event','title','is_active','created_on']
        verbose_name = 'Sự kiện-5-các Ban'
        verbose_name_plural = 'Sự kiện-5-các Ban'

class EventBoardAndMember(models.Model):
    member = models.ForeignKey(CustomUserModel,verbose_name='Thành viên',related_name='event_board_member_leaders', on_delete=models.CASCADE)
    event_board = models.ForeignKey(EventBoard,verbose_name='Thuộc ban',related_name='event_board_member_board', on_delete=models.CASCADE)
    member_type = models.BooleanField('Chức vụ',choices=membership_type,blank=True, null=True,default=False)
    is_scorer = models.BooleanField('Người chấm điểm',blank=True, null=True,default=False)
    is_active = models.BooleanField('Còn phụ trách',blank=True, null=True,default=False)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='event_board_member_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_board_member_updated_user',default=None,blank=True,null=True)

    class Meta:
        verbose_name = 'Sự kiện-5-các Ban-thành viên'
        verbose_name_plural = 'Sự kiện-5-các Ban-thành viên'
        ordering = ('is_active','event_board','member','member_type',)

    def __str__(self):
        return f'{self.event_board.title} : {self.member.full_name}'

class EventBoardTask(models.Model):
    title = models.CharField('Tiêu đề',blank=True, null=True,default='',max_length=300)
    slug = models.CharField('slug',blank=True, null=True,default='',max_length=400)
    sequence = models.CharField('Ưu tiên',default='2',choices=priority_choice,max_length=4)
    from_date_time= models.DateTimeField('Bắt đầu từ', default=timezone.now)
    to_date_time= models.DateTimeField('Đến khi', default=timezone.now)
    board = models.ForeignKey(EventBoard,verbose_name='Ban',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='event_board_task')
    board_member = models.ForeignKey(EventBoardAndMember,verbose_name='Đảm nhận',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='event_board_task_member')
    note = models.CharField('Ghi chú',max_length=500,blank=True,default='')
    status = models.CharField(max_length=3,choices=task_statuses,default=NOT_YET,null=True,blank=True)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='event_board_task_created_user')
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_board_task_updated_user',default=None,blank=True,null=True)
 
    class Meta:
        ordering = ['board','from_date_time','to_date_time','status','is_active']
        verbose_name = 'Sự kiện-5-các Ban-nhiệm vụ'
        verbose_name_plural = 'Sự kiện-5-các Ban-nhiệm vụ'
    
    def __str__(self):
        return f'{self.board.name}-{self.title}'


class EventGroup(models.Model):
    event = models.ForeignKey(Event,verbose_name='Sự kiện',related_name='event_group_event',on_delete=models.CASCADE)
    name = models.CharField('Tên nhóm',max_length=200)
    slug = models.CharField('Slug',max_length=100)
    image_url = models.ImageField('Hình ảnh',null=True,blank=True,upload_to='images/event')
    facebook_link = models.TextField('Facebook group link',null=True,blank=True,default='',help_text='Link facebook của đội chơi',max_length=500)
    drive_link = models.TextField('Link ảnh drive',null=True,blank=True,default='',help_text='Link ảnh drive của nhóm',max_length=500)
    is_active = models.BooleanField('Hoạt động',default=True, blank=True)    
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_group_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_group_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.event.title}-{self.name}'

    class Meta:
        ordering = ['event','name','is_active','created_on']
        verbose_name = 'Sự kiện-6-Đội'
        verbose_name_plural = 'Sự kiện-6-Đội'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(EventGroup, self).save(*args, **kwargs)

class UserAndEventGroup(models.Model):
    member = models.ForeignKey(CustomUserModel,verbose_name='Thành viên',related_name='user_and_event_group_member', on_delete=models.CASCADE)
    event_group = models.ForeignKey(Church,verbose_name='Nhóm',related_name='user_and_event_group_group', on_delete=models.CASCADE)
    member_type = models.BooleanField('Chức vụ',choices=membership_type,blank=True, null=True,default=False)
    is_scorer = models.BooleanField('Người chấm điểm',blank=True, null=True,default=False)
    is_active = models.BooleanField('Còn phụ trách',blank=True, null=True,default=False)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='user_and_event_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='user_and_event_updated_user',default=None,blank=True,null=True)

    class Meta:
        verbose_name = 'Sự kiện-6-Đội-thành viên'
        verbose_name_plural = 'Sự kiện-6-Đội-thành viên'
        ordering = ('event_group','member','member_type','created_on')

    def __str__(self):
        return f'{self.event_group.name} : {self.member.full_name}'


class EventGroupScoreType(models.Model):
    title = models.CharField('Tên mục',max_length=200)
    slug = models.CharField('Slug',max_length=100)
    excerpt = models.TextField('Giải thích',null=True,blank=True,default='',help_text='Không quá 1000 ký tự',max_length=1000)
    is_active = models.BooleanField('Hoạt động',default=True, blank=True)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_group_score_type_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_group_score_type_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title','is_active','created_on']
        verbose_name = 'Sự kiện-7-chấm điểm phân loại'
        verbose_name_plural = 'Sự kiện-7-chấm điểm phân loại'

class EventGroupScore(models.Model):
    event_group = models.ForeignKey(EventGroup,verbose_name='Tên nhóm',related_name='event_group_score',on_delete=models.CASCADE)
    date = models.DateField('Ngày',blank=True, null=True,default = timezone.now)
    score_type = models.CharField(max_length=2,choices=score_type,default='+')
    score_amount = models.IntegerField(default=0)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    on_account = models.ForeignKey(EventGroupScoreType,verbose_name='Phân loại', on_delete=models.CASCADE,related_name='event_group_score_account')
    notes = models.TextField('Ghi chú',null=True,blank=True,default='',help_text='Không quá 500 ký tự',max_length=500)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_group_score_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_group_score_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['event_group','on_account','-date','-score_amount']
        verbose_name = 'Sự kiện-7-nhóm-chấm điểm'
        verbose_name_plural = 'Sự kiện-7-nhóm-chấm điểm'

class EventTransactionAccount(models.Model):
    title = models.CharField('Tên mục',max_length=200)
    slug = models.CharField('Slug',max_length=100)
    excerpt = models.TextField('Giải thích',null=True,blank=True,default='',help_text='Không quá 1000 ký tự',max_length=1000)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_transaction_type_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_transaction_type_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title','created_on']
        verbose_name = 'Sự kiện-8-giao dịch phân loại'
        verbose_name_plural = 'Sự kiện-8-giao dịch phân loại'

class EventTransaction(models.Model):
    event = models.ForeignKey(Event,verbose_name='Sự kiện',related_name='event_transaction_detail',on_delete=models.CASCADE)
    date = models.DateField('Ngày',blank=True, null=True,default = timezone.now)
    transaction_type = models.CharField(max_length=2,choices=trasaction_type,default='I')
    transaction_amount = models.IntegerField(default=0)
    on_account = models.ForeignKey(EventTransactionAccount,verbose_name='Phân loại', on_delete=models.CASCADE,related_name='event_transaction_account')
    on_board = models.ForeignKey(EventBoard,verbose_name='Thuộc Ban', on_delete=models.CASCADE,related_name='event_transaction_board')
    notes = models.TextField('Ghi chú',null=True,blank=True,default='',help_text='Không quá 500 ký tự',max_length=500)
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='event_transaction_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='event_transaction_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.event.title}+{self.on_account.title}'

    class Meta:
        ordering = ['event','on_board','transaction_amount','transaction_type']
        verbose_name = 'Sự kiện-8-giao dịch'
        verbose_name_plural = 'Sự kiện-8-giao dịch'
