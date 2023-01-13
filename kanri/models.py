from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
from uuid import uuid4
from users.models import CustomUserModel
from lib.constant_choices import (group_type_choice,language_choice)
from lib.help import compressImage

# Create your models here.


class Language(models.Model):
    language_name = models.CharField('Tên Ngôn ngữ',help_text='Ngôn ngữ của Quốc gia',max_length=50)
    language_code = models.CharField('Mã',help_text='Mã theo i18n',max_length=3)
    language_en_name = models.CharField('Tên quốc tế',help_text='Tên theo tiếng anh',max_length=50)
    language_flag_small_url = models.ImageField('Hình ảnh',help_text='Hình ảnh minh hoạ',null=True,blank=True,upload_to='flags')
    language_flag_medium_url = models.ImageField('Hình ảnh',help_text='Hình ảnh minh hoạ',null=True,blank=True,upload_to='flags')

    def __str__(self):
        return self.language_name

    class Meta:
        verbose_name = 'Master-Ngôn ngữ'
        verbose_name_plural = 'Master-Ngôn ngữ'
        ordering = ('language_name',)

class Country(models.Model):
    japanese_name = models.CharField('Tên tiếng Nhật',max_length=50)
    english_name = models.CharField('Tên theo tiếng Anh',max_length=50)
    vietnamese_name = models.CharField('Tên theo tiếng Việt',max_length=50)
    code = models.CharField('Mã',max_length=6,blank=True, null=True)

    class Meta:
        verbose_name = 'Master-Đất nước'
        verbose_name_plural = 'Master-Đất nước'
        ordering = ('english_name',)

    def __str__(self):
        return self.english_name

class Region(models.Model):
    id = models.CharField(max_length = 50, primary_key = True, editable =  False)
    kanji = models.CharField('Tên Kanji',default='',max_length=50)
    name = models.CharField('Tên hiragana',max_length=50)
    nation = models.ForeignKey(Country,verbose_name='Quốc gia',on_delete=models.CASCADE)
    code = models.CharField('Mã',max_length=3,blank=True, null=True)

    class Meta:
        verbose_name = 'Master-Vùng'
        verbose_name_plural = 'Master-Vùng'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.name.lower()
        super(Region, self).save(*args, **kwargs)

class Province(models.Model):
    id = models.CharField(max_length = 50, primary_key = True, editable = False)
    kanji = models.CharField('Tên Kanji',default='',max_length=50)
    name = models.CharField('Tên hiragana',max_length=50)
    region = models.ForeignKey(Region,verbose_name='Vùng',on_delete=models.CASCADE)
    code = models.CharField('Mã',max_length=3,blank=True, null=True)

    class Meta:
        verbose_name = 'Master-Tỉnh'
        verbose_name_plural = 'Master-Tỉnh'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.name.lower()
        super(Province, self).save(*args, **kwargs)

class Facility(models.Model):
    kanji = models.CharField('Tên Kanji',default='',max_length=50)
    name = models.CharField('Tên Hiragana',help_text='Tên',max_length=200)
    image = models.ImageField('Hình ảnh',help_text='Hình ảnh đại diện',null=True,blank=True,upload_to='images')
    introduction = HTMLField('Giới thiệu',help_text='Mô tả sơ lược về Nhà thờ',blank=True)
    url = models.CharField('Web URL',help_text='Link liên kết',max_length=100, default='',blank=True)
    phone = models.CharField('Điện thoại',help_text='Số điện thoại',max_length=15, default='',blank=True)
    email = models.CharField('Email',help_text='Địa chỉ email',max_length=50, default='',blank=True)
    region = models.ForeignKey(Region,verbose_name='Vùng',default=None,blank=True,null=True,on_delete=models.CASCADE)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,on_delete=models.CASCADE)
    address = models.CharField('Địa chỉ',help_text='Địa chỉ',max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(Facility, self).save(*args, **kwargs)

class Church(models.Model):
    kanji = models.CharField('Tên Kanji',help_text='Tên Kanji', default='',max_length=200)
    name = models.CharField('Tên Hiragana',help_text='Tên Hiragana', default='',max_length=200)
    image = models.ImageField('Hình ảnh',help_text='Hình ảnh đại diện',null=True,blank=True,upload_to='images')
    introduction = HTMLField('Giới thiệu',help_text='Mô tả sơ lược về Nhà thờ',blank=True)
    url = models.CharField('Web URL',help_text='Link liên kết',max_length=100, default='',blank=True)
    phone = models.CharField('Điện thoại',help_text='Số điện thoại',max_length=15, default='',blank=True)
    email = models.CharField('Email',help_text='Địa chỉ email',max_length=50, default='',blank=True)
    language = models.CharField('Ngôn ngữ',max_length=50,choices=language_choice,default='jp')
    language1 = models.CharField('Ngôn ngữ phụ',max_length=50,choices=language_choice,default='vi')
    region = models.ForeignKey(Region,verbose_name='Vùng',default=None,blank=True,null=True,on_delete=models.CASCADE)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,on_delete=models.CASCADE)
    address = models.CharField('Địa chỉ',help_text='Địa chỉ',max_length=400)
    google_map_link = models.CharField('googlemap link',max_length=500)
    notice_on_map = HTMLField('Thông báo',help_text='Nội dung hiển thị trên Map',null=True,blank=True,default = '')
    geo_lon = models.FloatField('Kinh độ',help_text='Kinh độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_lat = models.FloatField('Vĩ độ',help_text='Vĩ độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_hash = models.CharField('geo_hash',max_length=30, default='',blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='church_created_user')
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='church_updated_user',default=None,blank=True,null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Nhà thờ'
        verbose_name_plural = 'Nhà thờ'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(Church, self).save(*args, **kwargs)

class ChurchImages(models.Model):
    title = models.CharField('Title',max_length=120)
    image = models.ImageField('Image',null=True,blank=True,upload_to='images/church/')
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    created_on = models.DateTimeField('Ngày tạo',auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='church_image_created_user')

    def __str__(self):
        return f'{self.image_title} : {self.id}'
    
    class Meta:
        ordering = ['created_on']
        verbose_name = 'Nhà thờ ảnh'
        verbose_name_plural = 'Nhà thờ ảnh'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(ChurchImages, self).save(*args, **kwargs)

class Father(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    user = models.OneToOneField(CustomUserModel,verbose_name='Tài khoản', on_delete=models.CASCADE)
    introduction = HTMLField('Giới thiệu',default='',blank=True,null=True)
    facebook = models.CharField('Link facebook',default='',blank=True,null=True,max_length=400)
    address = models.CharField('Địa chỉ hiện tại',default='',blank=True,max_length=300)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',null=True,default=None,blank=True,on_delete=models.CASCADE)
    phone_number = models.CharField('Số điện thoại',default='',blank=True, null=True,max_length=12)
    account_confimred = models.BooleanField('Xác minh',blank=True, null=True,default=False)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='father_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='father_updated_user',default=None,blank=True,null=True)

    class Meta:
        verbose_name = 'User-Quý cha'
        verbose_name_plural = 'User-Quý cha'
        unique_together = ('user','address')
        ordering = ('created_on',)

    def __str__(self):
        return f'{self.user.full_name}'

class FatherAndChurch(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    father = models.ForeignKey(Father,verbose_name='Cha', on_delete=models.CASCADE)
    church = models.ForeignKey(Church,verbose_name='Nhà thờ', on_delete=models.CASCADE)
    from_date = models.DateField('Từ ngày',blank=True, null=True,auto_now = True)
    to_date = models.DateField('Đến ngày',blank=True, null=True,auto_now = True)
    is_active = models.BooleanField('Còn phụ trách',blank=True, null=True,default=False)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='father_and_church_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='father_and_church_updated_user',default=None,blank=True,null=True)

    class Meta:
        verbose_name = 'Cha tại nhà thờ'
        verbose_name_plural = 'Cha tại nhà thờ'
        ordering = ('is_active','father','church__name',)

    def __str__(self):
        return f'{self.father.full_name} : {self.church.name}'

class Community(models.Model):
    name = models.CharField('Tên nhóm',help_text='Tên nhóm',max_length=200)
    name_jp = models.CharField('Tên tiếng Nhật',help_text='Tên nhóm',default='',max_length=200)
    slug = models.CharField('Slug',default='',max_length=200)
    image = models.ImageField('Hình ảnh',help_text='Hình ảnh đại diện',null=True,blank=True,upload_to='images/group')
    type = models.CharField('Phân loại',help_text='Cộng đoàn hoặc nhóm giới trẻ',max_length=10,default='group',choices=group_type_choice)
    introduction = HTMLField('Giới thiệu',help_text='Mô tả sơ lược về nhóm',blank=True)
    url = models.CharField('Facebook URL',help_text='Link liên kết facebook',max_length=100, default='',blank=True)
    email = models.CharField('Email',help_text='Địa chỉ email',max_length=50 ,null=True, default='',blank=True)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,on_delete=models.CASCADE,related_name='community_province')
    church = models.ForeignKey(Church,verbose_name='Nhà thờ sinh hoạt', on_delete=models.CASCADE)
    address = models.CharField('Địa chỉ sinh hoạt',help_text='Địa chỉ',max_length=400)
    google_map_link = models.CharField('googlemap link',max_length=500)
    is_active = models.BooleanField('Còn hoạt động',blank=True, null=True,default=False)
    notice_on_map = HTMLField('Thông báo',help_text='Nội dung hiển thị trên Map',null=True,blank=True,default = '')
    geo_lon = models.FloatField('Kinh độ',help_text='Kinh độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_lat = models.FloatField('Vĩ độ',help_text='Vĩ độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_hash = models.CharField('geo_hash',max_length=30,null=True, default='',blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='community_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='community_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name','province','created_on']
        verbose_name = 'Cộng đoàn, nhóm'
        verbose_name_plural = 'Cộng đoàn, nhóm'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(Community, self).save(*args, **kwargs)

class RepresentativeResponsibility(models.Model):
    name = models.CharField('Tên',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    is_active = models.BooleanField('Hoat dong',default=True, blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='representative_resp_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='representative_resp_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Master-Representative responsibility'
        verbose_name_plural = 'Master-Representative responsibilities'

class Representative(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    user = models.OneToOneField(CustomUserModel,verbose_name='Tài khoản', on_delete=models.CASCADE)
    introduction = HTMLField('Giới thiệu',default='',blank=True,null=True)
    facebook = models.CharField('Link facebook',default='',blank=True,null=True,max_length=400)
    address = models.CharField('Địa chỉ hiện tại',default='',blank=True,null=True,max_length=300)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,on_delete=models.CASCADE)
    phone_number = models.CharField('Số điện thoại',default='',blank=True, null=True,max_length=12)
    account_confimred = models.BooleanField('Xác minh',blank=True, null=True,default=False)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True, editable=False)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='representative_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='representative_updated_user',default=None,blank=True,null=True)

    class Meta:
        verbose_name = 'User-Representative'
        verbose_name_plural = 'User-Representatives'
        ordering = ('-created_on',)

    def __str__(self):
        return f'{self.user.full_name}'

class RepresentativeAndCommunity(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    representative = models.ForeignKey(Representative,verbose_name='Truong', on_delete=models.CASCADE)
    responsibility = models.ForeignKey(RepresentativeResponsibility,verbose_name='Trach nhiem',on_delete=models.CASCADE)
    community = models.ForeignKey(Community,verbose_name='Nhom', on_delete=models.CASCADE)
    from_date = models.DateField('Từ ngày',blank=True, null=True,default=timezone.now)
    to_date = models.DateField('Đến ngày',blank=True, null=True,default=timezone.now)
    is_active = models.BooleanField('Còn phụ trách',blank=True, null=True,default=False)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='representative_comm_created_user',default=None,blank=True,null=True,editable=False)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='representative_comm_updated_user',default=None,blank=True,null=True,)

    class Meta:
        verbose_name = 'Communnity and representative'
        verbose_name_plural = 'Master-Communnity and representatives'
        ordering = ('is_active','community','responsibility','representative','-from_date','-to_date')

    def __str__(self):
        return f'{self.representative.user.full_name} : {self.community.name}'

class UserProfile(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    user = models.OneToOneField(CustomUserModel,verbose_name='Tài khoản', on_delete=models.CASCADE,related_name='profile_user')
    facebook = models.CharField('Link facebook', null=True,default=None,blank=True,max_length=400)
    province = models.ForeignKey(Province,verbose_name='Tỉnh', null=True,default=None,blank=True,on_delete=models.CASCADE,related_name='user_profile_province')
    community = models.ForeignKey(Community,verbose_name='Cộng đoàn, Nhóm', null=True,default=None,blank=True,on_delete=models.CASCADE,related_name='user_profile_community')
    address = models.CharField('Địa chỉ', null=True,default=None,blank=True,max_length=300)
    phone_number = models.CharField('Số điện thoại',default='',blank=True, null=True,max_length=12)
    is_active = models.BooleanField('Còn phụ trách',blank=True, null=True,default=False)
    account_confimred = models.BooleanField('Xác minh',blank=True, null=True,default=False)
    code = models.CharField('Mã xác nhận',default='', null=True,blank=True,max_length=20)
    code_created_time = models.DateTimeField('Thời gian tạo mã',blank=True, null=True,auto_now = True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='profile_updated_user',default=None,blank=True,null=True)

    class Meta:
        verbose_name = "User-User profile"
        verbose_name_plural = "User-User profiles"
        ordering = ('user__username','user__email',)

    def __str__(self):
        return f'{self.user.username} : {self.user.full_name}'

