from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from tinymce.models import HTMLField
from users.models import CustomUserModel
from lib.constant_choices import (jp_region_choices,sequence_choise,priority_choice)
from kanri.models import Province, Church, Father

#image compression method
def compressImage(input_image):
    imageTemproary = Image.open(input_image)
    outputIoStream = BytesIO()
    imageTemproary.save(outputIoStream , format='JPEG', quality=80)
    outputIoStream.seek(0)
    input_image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % input_image.name.split('.')[0], 'image/jpg', sys.getsizeof(outputIoStream), None)
    return input_image

class Language(models.Model):
    language_name = models.CharField(_('Tên Ngôn ngữ'),max_length=100)
    language_code = models.CharField(_('Mã'),max_length=3)
    language_flag_small_url = models.ImageField(_('Hình ảnh'),null=True,blank=True,upload_to='flags')
    language_flag_medium_url = models.ImageField(_('Hình ảnh'),null=True,blank=True,upload_to='flags')

    def __str__(self):
        return self.language_name

# Create your models here.
class YoutubeVideo(models.Model):
    title = models.CharField('Chủ đề',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',max_length=500)
    youtube_url = models.CharField('Youtube link',max_length=200)
    isActive = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created on',auto_now = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_on']
        verbose_name = "Video youtube"
        verbose_name_plural = "Video youtube"

class Letter(models.Model):
    title = models.CharField('Chủ đề',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/letter')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 1000 ký tự',max_length=1000)
    content = HTMLField('Nội dung')
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    isActive = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created on',auto_now = True)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='letter_author', default=None, blank=True, null=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['created_on']
        verbose_name = "Thư mục vụ"
        verbose_name_plural = "Thư mục vụ"
    
    def save(self, *args, **kwargs):
        if self.image_url:
            self.image_url = compressImage(self.image_url)
        super(Letter, self).save(*args, **kwargs)

class PostType(models.Model):
    name = models.CharField('Tên',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    isActive = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created on',auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Loại bài viết"
        verbose_name_plural = "Loại bài viết"

class Post(models.Model):
    title = models.CharField('Chủ đề',max_length=300)
    slug = models.CharField('Slug',max_length=100)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',max_length=500)
    post_type = models.ForeignKey(PostType,verbose_name='Loại',on_delete=models.CASCADE)
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    isActive = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created on',auto_now = True)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='post_author', default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_on']
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(Post, self).save(*args, **kwargs)

class PostContent(models.Model):
    post = models.ForeignKey(Post,verbose_name='Bài',on_delete=models.CASCADE)
    chapter_title = models.CharField('Tên mục',max_length=200)
    slug = models.CharField('Slug',max_length=100)
    sequence = models.CharField('Thứ tự',default='0',choices=sequence_choise,max_length=4)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    chapter_summary = models.CharField('Tóm tắt',help_text='Không quá 500 ký tự',max_length=500)
    content = HTMLField('Nội dung')
    created_on = models.DateTimeField('Created on',auto_now = True)
    edited_by = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='content_author', default=None, blank=True, null=True)

    class Meta:
        ordering = ['post','sequence']
        verbose_name = "Nội dung bài viết"
        verbose_name_plural = "Nội dung bài viết"

class Aboutus(models.Model):
    title = models.CharField('Chủ đề',max_length=100)
    slug = models.CharField('Slug',max_length=100)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/announ')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',max_length=500)
    content = HTMLField('Nội dung')
    isActive = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created on',auto_now = True)
    author = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        ordering = ['created_on']
        verbose_name = "Giới thiệu"
        verbose_name_plural = "Giới thiệu"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(Aboutus, self).save(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField('Chủ đề',max_length=100)
    slug = models.CharField('Slug',max_length=200)
    image_url = models.ImageField('Hình ảnh',help_text='Hình ảnh phải được xử lý trước khi upload.',null=True, blank=True, upload_to='web_images/announ')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',default='',max_length=500)
    content = HTMLField('Nội dung')
    priority_choice = models.CharField('Ưu tiên',choices=priority_choice,default='2',max_length=10)
    isActive = models.BooleanField('Công khai',default=True, blank=True)
    from_date = models.DateField('Công khai từ',default=timezone.now)
    to_date = models.DateField('Công khai đến',default=timezone.now)
    event_date_time = models.DateTimeField('Event date time',default=timezone.now, blank=True, null=True)
    google_map_link = models.CharField('Google Map Link',null=True, blank=True,default='',max_length=200)
    register_link = models.CharField('Register Link',null=True, blank=True,default='',max_length=400)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created on',auto_now = True)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='announ_author', default=None, blank=True, null=True)
    updated_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='updated_user',default=None, blank=True, null=True)

    class Meta:
        ordering = ['priority_choice','isActive','created_on']
        verbose_name = "Thông báo chung"
        verbose_name_plural = "Thông báo chung"

    def __str__(self):
        return f'{self.slug}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)

        super(Announcement, self).save(*args, **kwargs)

class GospelRandom(models.Model):
    word = models.CharField(_('Câu nói'),default='',blank=True,max_length=500,help_text=_('Câu lời chúa'))
    content = models.TextField(_('Nội dung'),default='',max_length=2000,blank=True,help_text=_('Ý nghĩa câu Lời Chúa'))
    image_vertical = models.CharField(_('Hình ảnh dọc'),default='',max_length=200,help_text=_('Link driver, hình cho điện thoại'))
    image_horizontal = models.CharField(_('Hình ảnh khổ ngang'),default='',max_length=200,help_text=_('Link driver hình khổ ngang'))
    number_downloaded = models.SmallIntegerField(_('Số lượt tải về'),default=0,blank=True,null=True,help_text=_('Số lượt đã tải về'))
    status = models.BooleanField(_('Trạng thái'),help_text=_('Trạng thái hoạt động'),default=True,blank=True)
    created_date = models.DateTimeField(_('Ngày tạo'),default=timezone.now,blank=True)
    image_url = models.ImageField(_('Hình ảnh'),help_text=_('Hình ảnh hiển thị trên trang web'),null=True,blank=True,upload_to='gospel_img')

    def __str__(self):
        return f'{self.id}:{self.word}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.gospelrandom_img_url = compressImage(self.image_url)
        super(GospelRandom, self).save(*args, **kwargs)

class Gospel(models.Model):
    date = models.DateField('Ngày')
    title = models.CharField('Chủ đề',default='',max_length=300)
    slug = models.CharField('slug',blank=True, null=True,default='',max_length=400)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/gospel')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 300 ký tự',default='',max_length=300)
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_listened = models.SmallIntegerField('Số lượt nghe',default=0,blank=True,null=True,help_text='Số lượt nghe')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created on',auto_now = True)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='gospel_author', default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.date}: {self.title}'

    class Meta:
        ordering = ['-date']
        verbose_name = "Lời Chúa chủ đề"
        verbose_name_plural = "Lời Chúa chủ đề"
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)

        super(Gospel, self).save(*args, **kwargs)

class GospelContent(models.Model):
    gospel = models.ForeignKey(Gospel,verbose_name='Lời Chúa tiêu đề',on_delete=models.CASCADE,related_name='content_gospel')
    sequence = models.CharField('Thứ tự',default='0',choices=sequence_choise,max_length=4)
    chapter_title = models.CharField('Tiêu đề',default='',max_length=300)
    slug = models.CharField('slug',default='',max_length=400)
    chapter_reference = models.CharField('Tác giả',default='',max_length=100)
    content = HTMLField('Nội dung')
    created_on = models.DateTimeField('Created on',auto_now = True)

    def __str__(self):
        return f'{self.chapter_title}'

    class Meta:
        ordering = ['gospel','sequence']
        verbose_name = "Lời Chúa nội dung"
        verbose_name_plural = "Lời Chúa nội dung"

class GospelReflection(models.Model):
    gospel = models.ForeignKey(Gospel,verbose_name='Lời Chúa tiêu đề',on_delete=models.CASCADE,related_name='reflection_gospel')
    title = models.CharField('Tiêu đề',default='',max_length=300)
    slug = models.CharField('slug',default='',max_length=400)
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 300 ký tự',default='',max_length=300)
    content = HTMLField('Nội dung')
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_listened = models.SmallIntegerField('Số lượt nghe',default=0,blank=True,null=True,help_text='Số lượt nghe')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='reflection_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created on',auto_now = True)

    def __str__(self):
        return f'{self.title}: {self.title}'

    class Meta:
        ordering = ['gospel','-created_on']
        verbose_name = "Lời Chúa suy niệm"
        verbose_name_plural = "Lời Chúa suy niệm"

class MassDateSchedule(models.Model):
    date = models.DateField('Ngày')
    title = models.CharField('Tiêu đề',default='',max_length=300)
    slug = models.CharField('slug',blank=True, null=True,default='',max_length=400)
    gospel = models.ForeignKey(Gospel,verbose_name='Bài đọc',on_delete=models.CASCADE,related_name='mass_gospel',blank=True, null=True)
    
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
    created_on = models.DateTimeField('Created on',auto_now = True)

    class Meta:
        ordering = ['-from_date_time']
        verbose_name = "Lịch giải tội"
        verbose_name_plural = "Lịch giải tội"
    
    def __str__(self):
        return f'{self.from_date_time}-{self.to_date_time}'
