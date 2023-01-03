from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from tinymce.models import HTMLField
from users.models import CustomUserModel
from lib.constant_choises import (jp_region_choices,jp_province_choices,language_choice)
from kanri.models import Province, Church, Father

#image compression method
def compressImage(input_image):
    imageTemproary = Image.open(input_image)
    outputIoStream = BytesIO()
    imageTemproary.save(outputIoStream , format='JPEG', quality=60)
    outputIoStream.seek(0)
    input_image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" % input_image.name.split('.')[0], 'image/png', sys.getsizeof(outputIoStream), None)
    return input_image

class Language(models.Model):
    language_name = models.CharField(_('Tên Ngôn ngữ'),max_length=100)
    language_code = models.CharField(_('Mã'),max_length=3)
    language_flag_small_url = models.ImageField(_('Hình ảnh'),null=True,blank=True,upload_to='flags')
    language_flag_medium_url = models.ImageField(_('Hình ảnh'),null=True,blank=True,upload_to='flags')

    def __str__(self):
        return self.language_name

# Create your models here.
class Aboutus(models.Model):
    title = models.CharField('Title',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    imageUrl = models.ImageField('Image',null=True, blank=True, upload_to='web_images/announ')
    excerpt = HTMLField('Tóm tắt')
    content = HTMLField('Nội dung')
    isActive = models.BooleanField('Publish',default=True, blank=True)
    created_date = models.DateTimeField('Created on',default=timezone.now)
    created_user = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        ordering = ['created_date']
        verbose_name = "Giới thiệu"
        verbose_name_plural = "Giới thiệu"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.imageUrl:
                self.imageUrl = compressImage(self.imageUrl)
        super(Aboutus, self).save(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField('Title',max_length=100)
    slug = models.CharField('Slug',max_length=200)
    imageUrl = models.ImageField('Image',null=True, blank=True, upload_to='web_images/announ')
    excerpt = HTMLField('short description',null=True, blank=True,default='')
    content = HTMLField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=None, blank=True, null=True)
    isActive = models.BooleanField('Publish',default=True, blank=True)
    from_date = models.DateField('From Date',default=timezone.now)
    to_date = models.DateField('To Date',default=timezone.now)
    event_date_time = models.DateTimeField('Event date time',default=timezone.now)
    google_map_link = models.CharField('Google Map Link',null=True, blank=True,default='',max_length=200)
    register_link = models.CharField('Register Link',null=True, blank=True,default='',max_length=200)
    created_on = models.DateTimeField('Created on',default=timezone.now)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='author', default=None, blank=True, null=True)
    updated_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='updated_user',default=None, blank=True, null=True)

    class Meta:
        ordering = ['created_on']
        verbose_name = "Thông báo chung"
        verbose_name_plural = "Thông báo chung"

    def __str__(self):
        return f'{self.slug}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.imageUrl:
                self.imageUrl = compressImage(self.imageUrl)

        super(Announcement, self).save(*args, **kwargs)

class MassDateSchedule(models.Model):
    title = models.CharField('Tiêu đề',default='',max_length=300)
    slug = models.CharField('slug',blank=True, null=True,default='',max_length=400)
    date = models.DateField('Ngày',blank=True, null=True,auto_now = True)
    
    def __str__(self):
        return f'{self.date}: {self.title}'

    class Meta:
        ordering = ['-date']
        verbose_name = "Lịch Lễ"
        verbose_name_plural = "Lịch Lễ"

class MassTimeSchedule(models.Model):
    date_schedule = models.ForeignKey(MassDateSchedule,verbose_name='Thánh Lễ',on_delete=models.CASCADE)
    time = models.TimeField('Giờ',default='',max_length=300)
    father = models.ForeignKey(Father,verbose_name='Cha', on_delete=models.CASCADE,related_name='mass_father')
    church = models.ForeignKey(Church,verbose_name='Nhà thờ', on_delete=models.CASCADE,related_name='mass_church')
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,on_delete=models.SET_NULL,related_name='mass_province')
    notes = HTMLField('Ghi chú',blank=True, null=True,default='')

    class Meta:
        ordering = ['-date_schedule']
        verbose_name = "Lịch Lễ chi tiết"
        verbose_name_plural = "Lịch Lễ chi tiết"
    
    def __str__(self):
        return f'{self.date_schedule}-{self.time}'

class ConfessSchedule(models.Model):
    from_date_time= models.DateTimeField('Bắt đầu từ', default=timezone.now)
    to_date_time= models.DateTimeField('Đến khi', default=timezone.now)
    father = models.ForeignKey(Father,verbose_name='Cha', on_delete=models.CASCADE)
    notes= models.CharField('Ghi chú',max_length=500,blank=True,default='')
    church = models.ForeignKey(Church, on_delete=models.CASCADE,help_text='chọn Nhà thờ',blank=True,null=True,related_name='confess_church')
    publish= models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created on',default=timezone.now)

    class Meta:
        ordering = ['-from_date_time']
        verbose_name = "Lịch giải tội"
        verbose_name_plural = "Lịch giải tội"
    
    def __str__(self):
        return f'{self.from_date_time}-{self.to_date_time}'
