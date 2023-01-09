from django.contrib import admin
from django import forms
# Register your models here.
from .models import YoutubeVideo,Letter, PostType,Post,PostContent,Aboutus,Announcement,Gospel,GospelContent,GospelReflection, MassDateSchedule, MassTimeSchedule, ConfessSchedule


class LetterAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'is_active','created_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','post_type','is_active','created_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class PostContentAdmin(admin.ModelAdmin):
    list_display = ('post','chapter_title','created_on')
    list_filter = ('post',)
    search_fields = ['chapter_title', 'content']
    prepopulated_fields = {'slug': ('chapter_title',)}

    def save_model(self, request, obj, form, change):
        obj.edited_by = request.user
        obj.save()

class AboutusAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active','created_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title','created_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class GospelAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class GospelContentAdmin(admin.ModelAdmin):
    list_display = ('gospel','chapter_title','slug','created_on')
    search_fields = ['chapter_title', 'content','chapter_reference']
    prepopulated_fields = {'slug': ('chapter_title',)}

class GospelReflectionAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_on')
    search_fields = ['title', 'content','chapter_reference']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class MassDateScheduleScheduleAdmin(admin.ModelAdmin):
    list_display = ('date','date','slug','gospel')
    search_fields = ['date',]
    prepopulated_fields = {'slug': ('title',)}

class MassTimeScheduleAdmin(admin.ModelAdmin):
    list_display = ('date_schedule','time','father','church','province')
    list_filter = ('province',)
    search_fields = ['father', 'church']

class ConfessScheduleAdmin(admin.ModelAdmin):
    list_display = ('from_date_time','to_date_time','father','church', )
    list_filter = ('publish',)
    search_fields = ['father', 'church']

admin.site.register(YoutubeVideo)
admin.site.register(Letter,LetterAdmin)
admin.site.register(PostType)
admin.site.register(Post,PostAdmin)
admin.site.register(PostContent,PostContentAdmin)
admin.site.register(Aboutus,AboutusAdmin)
admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(Gospel,GospelAdmin)
admin.site.register(GospelContent,GospelContentAdmin)
admin.site.register(GospelReflection,GospelReflectionAdmin)
admin.site.register(MassDateSchedule,MassDateScheduleScheduleAdmin)
admin.site.register(MassTimeSchedule,MassTimeScheduleAdmin)
admin.site.register(ConfessSchedule,ConfessScheduleAdmin)