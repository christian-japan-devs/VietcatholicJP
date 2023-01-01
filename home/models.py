from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from users.models import CustomUserModel

# Create your models here.
class Aboutus(models.Model):
    title = models.CharField(_('Title'),max_length=100)
    slug = models.CharField(_('Slug'),max_length=100)
    imageUrl = models.ImageField(_('Image'),null=True, blank=True, upload_to='web_images/announ')
    short_introduce = HTMLField(_('short introduce'))
    content = HTMLField(_('Full content'))
    isActive = models.BooleanField(_('Publish'),default=True, blank=True)
    created_date = models.DateTimeField(_('Created on'),default=timezone.now)
    created_user = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        ordering = ['created_date']
        verbose_name = "Giới thiệu"
        verbose_name_plural = "Giới thiệu"