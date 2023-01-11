from django.contrib import admin

#Register your models here.
from .models import CustomUserModel

class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ('username','full_name','email','active','is_staff', 'is_superuser','created_on')
    list_filter = ('active','is_staff')
    search_fields = ['username','full_name','email']
    list_per_page = 50

admin.site.register(CustomUserModel,CustomUserModelAdmin)
