from django.contrib import admin

# Register your models here.
from .models import Aboutus, MassDateSchedule, MassTimeSchedule, ConfessSchedule

class AboutusAdmin(admin.ModelAdmin):
    list_display = ('title','slug','imageUrl','language', 'isActive','created_date')
    list_filter = ('isActive',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class MassTimeScheduleAdmin(admin.ModelAdmin):
    list_display = ('date_schedule','time','father','church','province')
    list_filter = ('province',)
    search_fields = ['father', 'church']

class ConfessScheduleAdmin(admin.ModelAdmin):
    list_display = ('from_date_time','to_date_time','father','church', )
    list_filter = ('publish',)
    search_fields = ['father', 'church']

admin.site.register(MassDateSchedule)
admin.site.register(MassTimeSchedule,MassTimeScheduleAdmin)
admin.site.register(ConfessSchedule,ConfessScheduleAdmin)