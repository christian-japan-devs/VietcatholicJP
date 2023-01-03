from django.db import models
from django.utils import timezone
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserModelManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """Create a custom user with the given fields"""
        user = self.model(
            username = username, 
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password = password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(max_length = 32, default = uuid4, primary_key = True, editable = False)
    username = models.CharField(max_length = 32, unique = True, null = False, blank = False)
    email = models.CharField(max_length = 100, unique = True, null = False, blank = False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['email']

    active = models.BooleanField(default = True)

    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    created_on  = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now = True)

    objects = CustomUserModelManager()

    class Meta:
        verbose_name = "User"
        ordering = ('-created_on','-username',)

class Profile(models.Model):
    id = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    user = models.OneToOneField(CustomUserModel,verbose_name='Tài khoản', on_delete=models.CASCADE)
    saint_name = models.CharField('Tên thánh',max_length=30)
    full_name = models.CharField('Họ tên',max_length=100)
    image = models.ImageField('Hình đại diện',default='default.jpg',null=True, upload_to='pics')
    facebook = models.CharField('Link facebook',default='',max_length=400)
    address = models.CharField('Địa chỉ',default='',max_length=300)
    phone_number = models.CharField('Số điện thoại',default='',blank=True, null=True,max_length=12)
    last_update_time = models.DateField('Lần cuối truy cập',blank=True, null=True,auto_now = True)
    account_confimred = models.BooleanField('Xác minh',blank=True, null=True,default=False)
    code = models.CharField('Mã xác nhận',default='',blank=True,max_length=20)

    class Meta:
        verbose_name = "User profile"
        unique_together = ('user','full_name','address')
        ordering = ('user__username','user__email',)

    def __str__(self):
        return f'{self.user.username} : {self.full_name} : {self.user.email}'

    def save(self, *args, **kwargs):
        if not self.id:
            print(self.id)
            if(self.image.name != 'default.jpg'):
                self.image = self.compressImage(self.image)
        super(Profile, self).save(*args, **kwargs)

    def compressImage(self,image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (300,300) )
        imageTemproaryResized.save(outputIoStream , format='PNG', quality=40)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.png" % image.name.split('.')[0], 'image/png', sys.getsizeof(outputIoStream), None)
        return image
