from django.contrib import admin

# Register your models here.
from .models import Aboutus

class AboutusAdmin(admin.ModelAdmin):
    list_display = ('title','slug','imageUrl','language', 'isActive','created_date')
    list_filter = ('isActive',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}