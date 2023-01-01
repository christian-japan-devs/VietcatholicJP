from django.db import models
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

    is_staff = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = True)

    created_on  = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now = True)

    objects = CustomUserModelManager()

    class Meta:
        verbose_name = "User"
        ordering = ('-created_on','-username',)
