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
            email = email,
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
    userId = models.CharField(max_length = 40, default = uuid4, primary_key = True, editable = False)
    username = models.CharField(max_length = 32, unique = True, null = False, blank = False)
    email = models.CharField(max_length = 100, unique = True, null = False, blank = False)
    saint_name = models.CharField('Tên thánh',null = True, blank = True,default='', max_length=100)
    full_name = models.CharField('Họ tên',null = True, blank = True,default='', max_length=200)
    image = models.ImageField('Hình đại diện',default='default.jpg',null=True, blank = True, upload_to='images/users')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['email']

    active = models.BooleanField(null = True, blank = True,default = True)

    is_staff = models.BooleanField(null = True, blank = True,default = False)
    is_superuser = models.BooleanField(null = True, blank = True,default = False)

    created_on  = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    updated_on = models.DateTimeField(null = True, blank = True,auto_now = True)

    objects = CustomUserModelManager()

    class Meta:
        verbose_name = "User"
        ordering = ('-created_on','-username',)

    def __str__(self):
        return f'{self.username}-{self.full_name}'
    
    def save(self, *args, **kwargs):
        if(self.image.name != 'default.jpg'):
            if not self.image:
                self.image = self.compressImage(self.image)
        super(CustomUserModel, self).save(*args, **kwargs)

    def compressImage(self,image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream , format='JPEG', quality=80)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpg', sys.getsizeof(outputIoStream), None)
        return image
