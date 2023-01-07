from django.db import models
from users.models import CustomUserModel
from tinymce.models import HTMLField
from django.utils import timezone
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from uuid import uuid4
from lib.constant_choices import (jp_region_choices,jp_province_choices,priority_choice,group_type_choice,language_choice)

# Create your models here.
#image compression method
def compressImage(input_image):
    imageTemproary = Image.open(input_image)
    outputIoStream = BytesIO()
    imageTemproary.save(outputIoStream , format='JPEG', quality=60)
    outputIoStream.seek(0)
    input_image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" % input_image.name.split('.')[0], 'image/png', sys.getsizeof(outputIoStream), None)
    return input_image

class Language(models.Model):
    language_name = models.CharField('Tên Ngôn ngữ',help_text='Ngôn ngữ của Quốc gia',max_length=50)
    language_code = models.CharField('Mã',help_text='Mã theo i18n',max_length=3)
    language_en_name = models.CharField('Tên quốc tế',help_text='Tên theo tiếng anh',max_length=50)
    language_flag_small_url = models.ImageField('Hình ảnh',help_text='Hình ảnh minh hoạ',null=True,blank=True,upload_to='flags')
    language_flag_medium_url = models.ImageField('Hình ảnh',help_text='Hình ảnh minh hoạ',null=True,blank=True,upload_to='flags')

    def __str__(self):
        return self.language_name

class Country(models.Model):
    japanese_name = models.CharField('Tên tiếng Nhật',max_length=50)
    english_name = models.CharField('Tên theo tiếng Anh',max_length=50)
    vietnamese_name = models.CharField('Tên theo tiếng Việt',max_length=50)
    code = models.CharField('Mã',max_length=6,blank=True, null=True)

    class Meta:
        verbose_name = "Đất nước"
        verbose_name_plural = "Đất nước"
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
        verbose_name = "Vùng"
        verbose_name_plural = "Vùng"
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
        verbose_name = "Tỉnh"
        verbose_name_plural = "Tỉnh"
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
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
    
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
    language = models.CharField('Ngôn ngữ',max_length=50,choices=language_choice,default="jp")
    language1 = models.CharField('Ngôn ngữ phụ',max_length=50,choices=language_choice,default="vi")
    region = models.ForeignKey(Region,verbose_name='Vùng',default=None,blank=True,null=True,on_delete=models.CASCADE)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,on_delete=models.CASCADE)
    address = models.CharField('Địa chỉ',help_text='Địa chỉ',max_length=400)
    google_map_link = models.CharField('googlemap link',max_length=500)
    notice_on_map = HTMLField('Thông báo',help_text='Nội dung hiển thị trên Map',null=True,blank=True,default = "")
    geo_lon = models.FloatField('Kinh độ',help_text='Kinh độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_lat = models.FloatField('Vĩ độ',help_text='Vĩ độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_hash = models.CharField('geo_hash',max_length=30, default='',blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Nhà thờ"
        verbose_name_plural = "Nhà thờ"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(Church, self).save(*args, **kwargs)

class ChurchImages(models.Model):
    title = models.CharField('Title',max_length=120)
    image = models.ImageField('Image',null=True,blank=True,upload_to='images/church/')
    church = models.ForeignKey(Church, on_delete=models.CASCADE)
    created_on = models.DateTimeField('Ngày tạo',auto_now = True)
    created_user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='created_user')

    def __str__(self):
        return f'{self.image_title} : {self.id}'
    
    class Meta:
        ordering = ['created_on']
        verbose_name = "Ảnh nhà thờ"
        verbose_name_plural = "Ảnh nhà thờ"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(ChurchImages, self).save(*args, **kwargs)

class Father(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    user = models.OneToOneField(CustomUserModel,verbose_name='Tài khoản', on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility,verbose_name='Tên nơi thuộc về', on_delete=models.CASCADE)
    introduction = HTMLField('Giới thiệu')
    facebook = models.CharField('Link facebook',default='',max_length=400)
    address = models.CharField('Địa chỉ hiện tại',default='',max_length=300)
    phone_number = models.CharField('Số điện thoại',default='',blank=True, null=True,max_length=12)
    last_update_time = models.DateField('Lần cuối truy cập',blank=True, null=True,auto_now = True)
    account_confimred = models.BooleanField('Xác minh',blank=True, null=True,default=False)

    class Meta:
        verbose_name = "Quý cha"
        verbose_name_plural = "Quý cha"
        unique_together = ('user','address')
        ordering = ('last_update_time',)

    def __str__(self):
        return f'{self.user.full_name}'

class FatherAndChurch(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    father = models.ForeignKey(Father,verbose_name='Cha', on_delete=models.CASCADE)
    church = models.ForeignKey(Church,verbose_name='Nhà thờ', on_delete=models.CASCADE)
    from_date = models.DateField('Từ ngày',blank=True, null=True,auto_now = True)
    to_date = models.DateField('Đến ngày',blank=True, null=True,auto_now = True)
    is_active = models.BooleanField('Còn phụ trách',blank=True, null=True,default=False)

    class Meta:
        verbose_name = "Cha tại nhà thờ"
        verbose_name_plural = "Cha tại nhà thờ"
        ordering = ('is_active','father','church__name',)

    def __str__(self):
        return f'{self.father.full_name} : {self.church.name}'

class Community(models.Model):
    name = models.CharField('Tên nhóm',help_text='Tên nhóm',max_length=200)
    name_jp = models.CharField('Tên tiếng Nhật',help_text='Tên nhóm',default='',max_length=200)
    image = models.ImageField('Hình ảnh',help_text='Hình ảnh đại diện',null=True,blank=True,upload_to='images/group')
    type = models.CharField('Phân loại',help_text='Cộng đoàn hoặc nhóm giới trẻ',max_length=10,default='group',choices=group_type_choice)
    introduction = HTMLField('Giới thiệu',help_text='Mô tả sơ lược về nhóm',blank=True)
    url = models.CharField('Facebook URL',help_text='Link liên kết facebook',max_length=100, default='',blank=True)
    email = models.CharField('Email',help_text='Địa chỉ email',max_length=50 ,null=True, default='',blank=True)
    region = models.ForeignKey(Region,verbose_name='Vùng',default=None,blank=True,null=True,on_delete=models.CASCADE)
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,on_delete=models.CASCADE)
    church = models.ForeignKey(Church,verbose_name='Nhà thờ sinh hoạt', on_delete=models.CASCADE)
    address = models.CharField('Địa chỉ sinh hoạt',help_text='Địa chỉ',max_length=400)
    google_map_link = models.CharField('googlemap link',max_length=500)
    notice_on_map = HTMLField('Thông báo',help_text='Nội dung hiển thị trên Map',null=True,blank=True,default = "")
    geo_lon = models.FloatField('Kinh độ',help_text='Kinh độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_lat = models.FloatField('Vĩ độ',help_text='Vĩ độ theo bản đồ Google',default=0.0,blank=True,null=True)
    geo_hash = models.CharField('geo_hash',max_length=30,null=True, default='',blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name','created_on']
        verbose_name = "Cộng đoàn, nhóm"
        verbose_name_plural = "Cộng đoàn, nhóm"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image:
                self.image = compressImage(self.image)
        super(Community, self).save(*args, **kwargs)