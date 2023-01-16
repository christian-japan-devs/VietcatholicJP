from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from users.models import CustomUserModel
from lib.constant_choices import (sequence_choise,priority_choice,language_choice,year_choice,aboutus_types)
from lib.help import compressImage
from kanri.models import Province, Church, Father, Language

# Create your models here.
class YoutubeVideo(models.Model):
    title = models.CharField('Chủ đề',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    excerpt = models.TextField('Tóm tắt',null=True,blank=True,default='',help_text='Không quá 500 ký tự',max_length=500)
    youtube_url = models.CharField('Youtube id',help_text='Lưu ý là id của video link phần XXXXXXXXX từ sau ?v=XXXXXXXXX',max_length=200)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Ngày tạo',blank=True,null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='youtube_link_created_user')
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='youtube_link_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_on','title']
        verbose_name = '99-Youtube video'
        verbose_name_plural = '99-Youtube videos'

class Letter(models.Model):
    title = models.CharField('Chủ đề',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/letter')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 1000 ký tự',max_length=1000)
    content = HTMLField('Nội dung')
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='letter_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='letter_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='letter_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['created_on']
        verbose_name = '01-Thư mục vụ'
        verbose_name_plural = '01-Thư mục vụ'
    
    def save(self, *args, **kwargs):
        if self.image_url:
            self.image_url = compressImage(self.image_url)
        super(Letter, self).save(*args, **kwargs)

class PostType(models.Model):
    name = models.CharField('Tên',max_length=200,help_text='Dài không quá 200 ký tự')
    slug = models.CharField('Slug',max_length=200)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='post_type_created_user')
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='post_type_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '02-Bài viết-01-phân loại'
        verbose_name_plural = '02-Bài viết-01-phân loại'

class Post(models.Model):
    title = models.CharField('Chủ đề',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    language = models.CharField('Ngôn ngữ',max_length=50,choices=language_choice,default='vi')
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',max_length=500)
    post_type = models.ForeignKey(PostType,verbose_name='Loại',on_delete=models.CASCADE)
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='post_author', default=None, blank=True, null=True)
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='post_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='post_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']
        verbose_name = '02-Bài viết-02-chủ đề'
        verbose_name_plural = '02-Bài viết-02-chủ đề'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(Post, self).save(*args, **kwargs)

class PostContent(models.Model):
    post = models.ForeignKey(Post,verbose_name='Bài',on_delete=models.CASCADE)
    chapter_title = models.CharField('Tên mục',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=200,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    sequence = models.CharField('Thứ tự',default='0',choices=sequence_choise,max_length=4)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    chapter_summary = models.CharField('Tóm tắt',default='',null=True, blank=True,help_text='Không quá 500 ký tự',max_length=500)
    content = HTMLField('Nội dung')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='post_content_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='post_content_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='post_content_updated_user',default=None,blank=True,null=True)

    class Meta:
        ordering = ['post','sequence','-created_on']
        verbose_name = '02-Bài viết-03-nội dung'
        verbose_name_plural = '02-Bài viết-03-nội dung'

class Aboutus(models.Model):
    type = models.CharField('Phan loai',choices=aboutus_types,default='vcj',max_length=300,help_text='Phan loai')
    title = models.CharField('Chủ đề',max_length=300,help_text='Dài không quá 300 ký tự')
    title_jp = models.CharField('Chủ đề tiếng Nhật',default='',blank=True,null=True,max_length=300,help_text='Dài không quá 300 ký tự')
    title_en = models.CharField('Chủ đề tiếng Anh',default='',blank=True,null=True,max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu') 
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/announ')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',default='',max_length=500)
    excerpt_jp = models.TextField('Tóm tắt tiếng Nhật',help_text='Không quá 500 ký tự',null=True, blank=True,default='',max_length=500)
    excerpt_en = models.TextField('Tóm tắt tiếng Anh',help_text='Không quá 500 ký tự',null=True, blank=True,default='',max_length=500)
    content = HTMLField('Nội dung')
    content_jp = HTMLField('Nội dung tiếng Nhật',default='',blank=True,null=True)
    content_en = HTMLField('Nội dung tiếng Anh',default='',blank=True,null=True)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='about_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='about_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='about_updated_user',default=None,blank=True,null=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = '80-Giới thiệu'
        verbose_name_plural = '80-Giới thiệu'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(Aboutus, self).save(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField('Chủ đề',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    image_url = models.ImageField('Hình ảnh',help_text='Hình ảnh phải được xử lý trước khi upload.',null=True, blank=True, upload_to='web_images/announ')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',default='',max_length=500)
    content = HTMLField('Nội dung')
    priority_choice = models.CharField('Ưu tiên',choices=priority_choice,default='2',max_length=10)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    from_date = models.DateField('Công khai từ',default=timezone.now)
    to_date = models.DateField('Công khai đến',default=timezone.now)
    event_date_time = models.DateTimeField('Event date time',default=timezone.now, blank=True, null=True)
    google_map_link = models.CharField('Google Map Link',null=True, blank=True,default='',max_length=200)
    register_link = models.CharField('Register Link',null=True, blank=True,default='',max_length=400)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='announ_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='announ_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='announ_updated_user',default=None, blank=True, null=True)

    class Meta:
        ordering = ['-priority_choice','is_active','-created_on']
        verbose_name = '70-Thông báo chung'
        verbose_name_plural = '70-Thông báo chung'

    def __str__(self):
        return f'{self.slug}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)

        super(Announcement, self).save(*args, **kwargs)

class GospelRandom(models.Model):
    word = models.CharField('Câu nói',default='',blank=True,max_length=500,help_text='Câu lời chúa')
    word_jp = models.CharField('Câu nói Japanese',default='',blank=True,max_length=500,help_text='Câu lời chúa')
    word_en = models.CharField('Câu nói English',default='',blank=True,max_length=500,help_text='Câu lời chúa')
    language = models.CharField('Ngôn ngữ',max_length=50,choices=language_choice,default='vi')
    content = models.TextField('Nội dung',default='',max_length=2000,blank=True,help_text='Ý nghĩa câu Lời Chúa')
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    image_vertical = models.CharField('Hình ảnh dọc',default='',max_length=200,help_text='Link driver, hình cho điện thoại')
    image_horizontal = models.CharField('Hình ảnh khổ ngang',default='',max_length=200,help_text='Link driver hình khổ ngang')
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    number_downloaded = models.SmallIntegerField('Số lượt tải về',default=0,blank=True,null=True,help_text='Số lượt đã tải về')
    is_active = models.BooleanField('Công khai',help_text='Trạng thái công khai',default=True,blank=True)
    image_url = models.ImageField('Hình ảnh',help_text='Hình ảnh hiển thị trên trang web',null=True,blank=True,upload_to='gospel_img')
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='gospel_random_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='gospel_random_updated_user',default=None,blank=True,null=True)

    class Meta:
        ordering = ['word','is_active','-created_on']
        verbose_name = '10-Câu lời Chúa'
        verbose_name_plural = '10-Câu lời Chúa'

    def __str__(self):
        return f'{self.id}:{self.word}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.gospelrandom_img_url = compressImage(self.image_url)
        super(GospelRandom, self).save(*args, **kwargs)

# Start Gospel

class Gospel(models.Model):
    date = models.DateField('Ngày')
    year_type = models.CharField('Năm phụng vụ',choices=year_choice,default='A',max_length=2)
    title = models.CharField('Chủ đề',default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_jp = models.CharField('Chủ đề tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_en = models.CharField('Chủ đề tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,default='',help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/gospel')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',default='',max_length=500)
    excerpt_jp = models.TextField('Tóm tắt tiếng Nhật',help_text='Không quá 500 ký tự',null=True, blank=True,default='',max_length=500)
    excerpt_en = models.TextField('Tóm tắt tiếng Anh',help_text='Không quá 500 ký tự',null=True, blank=True,default='',max_length=500)
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    audio_link_jp = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    audio_link_en = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_listened = models.SmallIntegerField('Số lượt nghe',default=0,blank=True,null=True,help_text='Số lượt nghe')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='gospel_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='gospel_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.date}: {self.title}'

    class Meta:
        ordering = ['-date','year_type','-created_on']
        verbose_name = '11-Lời Chúa-01-chủ đề'
        verbose_name_plural = '11-Lời Chúa-01-chủ đề'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(Gospel, self).save(*args, **kwargs)

class GospelContent(models.Model):
    gospel = models.ForeignKey(Gospel,verbose_name='Lời Chúa',on_delete=models.CASCADE,related_name='content_gospel')
    sequence = models.CharField('Thứ tự',default='0',choices=sequence_choise,max_length=4)
    chapter_title = models.CharField('Tiêu đề',default='',max_length=300,help_text='Dài không quá 300 ký tự')
    chapter_title_jp = models.CharField('Tiêu đề tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    chapter_title_en = models.CharField('Tiêu đề tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    chapter_reference = models.CharField('Tác giả',null=True, blank=True,default='',max_length=100)
    chapter_reference_jp = models.CharField('Tác giả tiếng Nhật',null=True, blank=True,default='',max_length=100)
    chapter_reference_en = models.CharField('Tác giả tiếng Anh',null=True, blank=True,default='',max_length=100)
    content = HTMLField('Nội dung')
    content_jp = HTMLField('Nội dung tiếng Nhật',null=True, blank=True,default='')
    content_en = HTMLField('Nội dung tiếng Anh',null=True, blank=True,default='')
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='gospel_content_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='gospel_content_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.chapter_title}'

    class Meta:
        ordering = ['gospel','sequence','-created_on']
        verbose_name = '11-Lời Chúa-02-nội dung'
        verbose_name_plural = '11-Lời Chúa-02-nội dung'

class CommuintyPrayer(models.Model):
    gospel = models.ForeignKey(Gospel,verbose_name='Lời Chúa',on_delete=models.CASCADE,related_name='gospel_community_prayer')
    title = models.CharField('Tiêu đề',default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_jp = models.CharField('Tiêu đề tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_en = models.CharField('Tiêu đề tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    content = HTMLField('Nội dung')
    content_jp = HTMLField('Nội dung tiếng Nhật',null=True, blank=True,default='')
    content_en = HTMLField('Nội dung tiếng Anh',null=True, blank=True,default='')
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='community_prayer_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='community_prayer_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.gospel.title}:{self.title}'

    class Meta:
        ordering = ['gospel','title','-created_on']
        verbose_name = '11-Lời Chúa-03- Lời nguyện giáo dân'
        verbose_name_plural = '11-Lời Chúa-03- Lời nguyện giáo dân'

class GospelReflection(models.Model):
    gospel = models.ForeignKey(Gospel,verbose_name='Lời Chúa',on_delete=models.CASCADE,related_name='reflection_gospel')
    title = models.CharField('Chủ đề',default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_jp = models.CharField('Chủ đề tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_en = models.CharField('Chủ đề tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    audio_link_jp = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    audio_link_en = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    language = models.CharField('Ngôn ngữ',max_length=50,choices=language_choice,default='vi')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',default='',max_length=500)
    excerpt_jp = models.TextField('Tóm tắt tiếng Nhật',help_text='Không quá 500 ký tự',null=True, blank=True,default='',max_length=500)
    excerpt_en = models.TextField('Tóm tắt tiếng Anh',help_text='Không quá 500 ký tự',null=True, blank=True,default='',max_length=500)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/gospel')
    content = HTMLField('Nội dung')
    content_jp = HTMLField('Nội dung tiếng Nhật',null=True, blank=True,default='')
    content_en = HTMLField('Nội dung tiếng Anh',null=True, blank=True,default='')
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_listened = models.SmallIntegerField('Số lượt nghe',default=0,blank=True,null=True,help_text='Số lượt nghe')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='reflection_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='gospel_reflection_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='gospel_reflection_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.gospel.title}:{self.title}'

    class Meta:
        ordering = ['gospel','-created_on']
        verbose_name = '11-Lời Chúa-04-suy niệm'
        verbose_name_plural = '11-Lời Chúa-04-suy niệm'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(GospelReflection, self).save(*args, **kwargs)


''' Start Caterism'''
class LessonType(models.Model):
    name = models.CharField('Tên',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Dài không quá 300 ký tự')
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='lesson_type_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='lesson_type_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '20-Giáo lý-01 phân loại'
        verbose_name_plural = '20-Giáo lý-01 phân loại'

class Lesson(models.Model):
    lesson_type = models.ForeignKey(LessonType,verbose_name='Phân loại',on_delete=models.CASCADE)
    lesson_no =  models.SmallIntegerField('Bài số',default=0)
    title = models.CharField('Chủ đề tên bài',max_length=300,help_text='Dài không quá 300 ký tự')
    title_jp = models.CharField('Chủ đề tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    title_en = models.CharField('Chủ đề tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=200,help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    excerpt = models.TextField('Tóm tắt',help_text='Không quá 500 ký tự',max_length=500)
    excerpt = models.TextField('Tóm tắt tiếng Nhật',null=True, blank=True,default='',help_text='Không quá 500 ký tự',max_length=500)
    excerpt = models.TextField('Tóm tắt tiếng Anh',null=True, blank=True,default='',help_text='Không quá 500 ký tự',max_length=500)
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='lesson_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='lesson_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['lesson_type','lesson_no','-created_on']
        verbose_name = '20-Giáo lý-02 chủ đề'
        verbose_name_plural = '20-Giáo lý-02 chủ đề'
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(Lesson, self).save(*args, **kwargs)

class LessonChapter(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='Bài',on_delete=models.CASCADE)
    chapter_no =  models.SmallIntegerField('Chương số',default=0)
    chapter_title = models.CharField('Tên chương',max_length=200,help_text='Dài không quá 200 ký tự')
    slug = models.CharField('Slug',max_length=200,help_text='Vui lòng chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    sequence = models.CharField('Thứ tự',default='0',choices=sequence_choise,max_length=4)
    image_url = models.ImageField('Hình ảnh',null=True, blank=True, upload_to='web_images/post')
    chapter_summary = models.CharField('Tóm tắt',default='',null=True, blank=True,help_text='Không quá 500 ký tự',max_length=500)
    content = HTMLField('Nội dung')
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='lesson_content_author', default=None, blank=True, null=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='lesson_content_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='lesson_content_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.lesson.title}-{self.chapter_title}'

    class Meta:
        ordering = ['lesson','sequence','-created_on']
        verbose_name = '20-Giáo lý-03 chương'
        verbose_name_plural = '20-Giáo lý-03 chương'

    def save(self, *args, **kwargs):
        if not self.id:
            if self.image_url:
                self.image_url = compressImage(self.image_url)
        super(LessonChapter, self).save(*args, **kwargs)

class LessonChapterQA(models.Model):
    chapter = models.ForeignKey(LessonChapter,verbose_name='Chương',on_delete=models.CASCADE)
    question_no =  models.SmallIntegerField('Câu hỏi số',default=0)
    question = models.TextField('Câu hỏi',max_length=1000,help_text='Dài không quá 1000 ký tự')
    answer = models.TextField('Câu trả lời',max_length=2000,help_text='Dài không quá 2000 ký tự')
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='lesson_chapter_qa_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='lesson_chapter_qa_updated_user',default=None,blank=True,null=True)

    class Meta:
        ordering = ['chapter','question_no','-created_on']
        verbose_name = '20-Giáo lý-04 chương câu hỏi'
        verbose_name_plural = '20-Giáo lý-04 chương câu hỏi'

class LessonQA(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='Bài',on_delete=models.CASCADE)
    question_no =  models.SmallIntegerField('Câu hỏi số',default=0)
    question = models.TextField('Câu hỏi',max_length=1000,help_text='Dài không quá 1000 ký tự')
    answer_1 = models.TextField('Đáp án A',max_length=1000,help_text='Dài không quá 1000 ký tự')
    answer_2 = models.TextField('Đáp án B',max_length=1000,help_text='Dài không quá 1000 ký tự',default='',blank=True,null=True)
    answer_3 = models.TextField('Đáp án C',max_length=1000,help_text='Dài không quá 1000 ký tự',default='',blank=True,null=True)
    answer_4 = models.TextField('Đáp án D',max_length=1000,help_text='Dài không quá 1000 ký tự',default='',blank=True,null=True)
    correct_answer =  models.TextField('Câu trả lời đúng',max_length=2,default='A')
    number_answered = models.SmallIntegerField('Số lượt làm',default=0,blank=True,null=True)
    number_correct = models.SmallIntegerField('Số lượt làm đúng',default=0,blank=True,null=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='lesson_qa_created_user', default=None, blank=True, null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='lesson_qa_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.lesson}- câu số {self.question_no}'

    class Meta:
        ordering = ['lesson','question_no','-created_on']
        verbose_name = '20-Giáo lý-04 Bài câu hỏi'
        verbose_name_plural = '20-Giáo lý-04 Bài câu hỏi'

''' End Caterism'''
''' Start Prayer'''
class PrayerType(models.Model):
    name = models.CharField('Tên',max_length=200,help_text='Dài không quá 200 ký tự')
    name_jp = models.CharField('Tên tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    name_en = models.CharField('Tên tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=200)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='prayer_type_created_user')
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='prayer_type_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '25-Kinh đọc-01-phân loại'
        verbose_name_plural = '25-Kinh đọc-01-phân loại'

class Prayer(models.Model):
    prayer_type = models.ForeignKey(PrayerType,default=None,verbose_name='Loại',on_delete=models.CASCADE)
    name = models.CharField('Tên',max_length=300,help_text='Dài không quá 300 ký tự')
    name_jp = models.CharField('Tên tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    name_en = models.CharField('Tên tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    audio_link_jp = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    audio_link_en = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    content = HTMLField('Nội dung')
    content_jp = HTMLField('Nội dung tiếng Nhật',null=True, blank=True,default='')
    content_en = HTMLField('Nội dung tiếng Anh',null=True, blank=True,default='')
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='prayer_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='prayer_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['prayer_type','name','-created_on']
        verbose_name = '25-Kinh đọc-02 nội dung'
        verbose_name_plural = '25-Kinh đọc-02 nội dung'

""""""

class CeremonyType(models.Model):
    name = models.CharField('Tên',max_length=300,help_text='Dài không quá 300 ký tự')
    name_jp = models.CharField('Tên tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    name_en = models.CharField('Tên tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300)
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='ceremony_type_created_user')
    created_on = models.DateTimeField('Created on',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Ngày cập nhật',help_text='Lần cuối cập nhật',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='ceremony_type_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return f'{self.name}-{self.name_jp}'

    class Meta:
        ordering = ['-created_on']
        verbose_name = '30-Nghi thức-01 phân loại'
        verbose_name_plural = '30-Nghi thức-01 phân loại'

class Ceremony(models.Model):
    type = models.ForeignKey(CeremonyType,default=None,verbose_name='Loại',on_delete=models.CASCADE)
    name = models.CharField('Tên',max_length=300,help_text='Dài không quá 300 ký tự')
    name_jp = models.CharField('Tên tiếng Nhật',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    name_en = models.CharField('Tên tiếng Anh',null=True, blank=True,default='',max_length=300,help_text='Dài không quá 300 ký tự')
    slug = models.CharField('Slug',max_length=300,help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    audio_link = models.CharField('Audio Link',null=True, blank=True,default='',max_length=400)
    audio_link_jp = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    audio_link_en = models.CharField('Audio Link tiếng Nhật',null=True, blank=True,default='',max_length=400)
    content = HTMLField('Nội dung')
    content_jp = HTMLField('Nội dung tiếng Nhật',null=True, blank=True,default='')
    content_en = HTMLField('Nội dung tiếng Anh',null=True, blank=True,default='')
    reference_link = models.CharField('Nguồn tham khảo Link',null=True, blank=True,default='',max_length=5000,help_text='Nếu có nhiều nguồn vui lòng thêm dấu ";" để phân cách các nguồn tham khảo.')
    is_active = models.BooleanField('Công khai',default=True, blank=True)
    number_readed = models.SmallIntegerField('Số lượt đọc',default=0,blank=True,null=True,help_text='Số lượt đọc')
    number_shared = models.SmallIntegerField('Số lượt chia sẻ',default=0,blank=True,null=True,help_text='Số lượt chia sẻ')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,related_name='ceremony_created_user',default=None,blank=True,null=True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='ceremony_updated_user',default=None,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['type','name','-created_on']
        verbose_name = '30-Nghi thức-02 nội dung'
        verbose_name_plural = '30-Nghi thức-02 nội dung'

class MassDateSchedule(models.Model):
    date = models.DateField('Ngày')
    title = models.CharField('Tiêu đề',default='',max_length=300)
    slug = models.CharField('Slug',max_length=300,default='',help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    gospel = models.ForeignKey(Gospel,verbose_name='Bài đọc',on_delete=models.CASCADE,related_name='mass_gospel',blank=True, null=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='mass_date_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='mass_date_updated_user',default=None,blank=True,null=True)
    
    def __str__(self):
        return f'{self.date}: {self.title}'

    class Meta:
        ordering = ['-date','-created_on']
        verbose_name = '40-Lịch Lễ-01 ngày'
        verbose_name_plural = '40-Lịch Lễ-01 ngày'

class MassTimeSchedule(models.Model):
    date_schedule = models.ForeignKey(MassDateSchedule,verbose_name='Thánh Lễ',related_name='time_schedule',on_delete=models.CASCADE)
    time = models.TimeField('Giờ',default='',max_length=300)
    language = models.CharField('Ngôn ngữ',max_length=50,choices=language_choice,default='vi')
    father = models.ForeignKey(Father,verbose_name='Cha', on_delete=models.CASCADE,related_name='mass_father')
    church = models.ForeignKey(Church,verbose_name='Nhà thờ', on_delete=models.CASCADE,related_name='mass_church')
    province = models.ForeignKey(Province,verbose_name='Tỉnh',default=None,blank=True,null=True,on_delete=models.SET_NULL,related_name='mass_province')
    notes = HTMLField('Ghi chú',blank=True, null=True,default='')
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='mass_time_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='mass_time_updated_user',default=None,blank=True,null=True)
 
    class Meta:
        ordering = ['-date_schedule']
        verbose_name = '40-Lịch Lễ-02 giờ chi tiết'
        verbose_name_plural = '40-Lịch Lễ-02 giờ chi tiết'
    
    def __str__(self):
        return f'{self.date_schedule}-{self.time}'

class ConfessSchedule(models.Model):
    title = models.CharField('Tiêu đề',blank=True, null=True,default='',max_length=300)
    slug = models.CharField('Slug',max_length=300,default='',help_text='Chỉnh lại phần tự sinh ra cho giống với title, * không dấu')
    from_date_time= models.DateTimeField('Bắt đầu từ', default=timezone.now)
    to_date_time= models.DateTimeField('Đến khi', default=timezone.now)
    father = models.ForeignKey(Father,verbose_name='Cha', on_delete=models.CASCADE)
    notes= models.CharField('Ghi chú',max_length=500,blank=True,default='')
    church = models.ForeignKey(Church, on_delete=models.CASCADE,help_text='chọn Nhà thờ',blank=True,null=True,related_name='confess_church')
    publish= models.BooleanField('Công khai',default=True, blank=True)
    created_user = models.ForeignKey(CustomUserModel,verbose_name='Người tạo',on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='confession_time_created_user')
    created_on = models.DateTimeField('Created',blank=True, null=True,auto_now_add = True)
    updated_on = models.DateTimeField('Updated',blank=True, null=True,auto_now = True)
    updated_user = models.ForeignKey(CustomUserModel,verbose_name='Người cập nhật',on_delete=models.CASCADE,related_name='confession_time_updated_user',default=None,blank=True,null=True)
 
    class Meta:
        ordering = ['-from_date_time']
        verbose_name = '41-Lịch giải tội'
        verbose_name_plural = '41-Lịch giải tội'
    
    def __str__(self):
        return f'{self.from_date_time}-{self.to_date_time}'