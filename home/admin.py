from django.contrib import admin
from django.utils import timezone
from django import forms
# Register your models here.
from .models import (YoutubeVideo,Letter, PostType,Post,PostContent,
                    Aboutus,Announcement,GospelRandom,Gospel,GospelContent,
                    GospelReflection, MassDateSchedule, MassTimeSchedule, ConfessSchedule,
                    LessonType,Lesson,LessonQA,LessonChapter,LessonChapterQA,PrayerType,
                    Prayer,CommuintyPrayer,CeremonyType,Ceremony)


class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title','excerpt', 'is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class LetterAdmin(admin.ModelAdmin):
    list_display = ('title','number_readed','number_shared', 'is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active','created_user')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','number_readed','number_shared','post_type','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active','created_user',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class PostContentAdmin(admin.ModelAdmin):
    list_display = ('post','title','title_jp','title_en','created_user','created_on','updated_user','updated_on')
    list_filter = ('post',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class AboutusAdmin(admin.ModelAdmin):
    list_display = ('title','number_readed','number_shared', 'is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title','number_readed','number_shared','from_date','to_date','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class GospelRandomAdmin(admin.ModelAdmin):
    list_display = ('word','number_downloaded','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['word', 'content']
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_downloaded','image_url','reference_link','content','word_en')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class GospelAdmin(admin.ModelAdmin):
    list_display = ('year_type','title','number_readed','number_shared','created_user','created_on','updated_user','updated_on')
    list_filter = ('year_type',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class GospelContentAdmin(admin.ModelAdmin):
    list_display = ('gospel','title','created_user','created_on','updated_user','updated_on')
    search_fields = ['title', 'content','chapter_reference']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class GospelReflectionAdmin(admin.ModelAdmin):
    list_display = ('title','number_readed','number_shared','author','created_on','updated_user','updated_on')
    search_fields = ['title', 'content','chapter_reference']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.created_user = request.created_user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class MassDateScheduleScheduleAdmin(admin.ModelAdmin):
    list_display = ('date','date','gospel','created_user','created_on','updated_user','updated_on')
    search_fields = ['date',]
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()
    
class MassTimeScheduleAdmin(admin.ModelAdmin):
    list_display = ('date_schedule','time','father','church','province','created_user','created_on','updated_user','updated_on')
    list_filter = ('province',)
    search_fields = ['father', 'church']
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class ConfessScheduleAdmin(admin.ModelAdmin):
    list_display = ('title','from_date_time','to_date_time','father','church','created_user','created_on','updated_user','updated_on' )
    list_filter = ('publish',)
    search_fields = ['father', 'church']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_type','title','number_readed','number_shared','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active','lesson_type',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class LessonChapterAdmin(admin.ModelAdmin):
    list_display = ('lesson','chapter_no','title','title_jp','title_en','created_user','created_on','updated_user','updated_on')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class LessonChapterQAAdmin(admin.ModelAdmin):
    list_display = ('chapter','question_no','question','number_readed','created_user','created_on','updated_user','updated_on')
    list_filter = ('chapter',)
    search_fields = ['question']
    exclude = ('number_readed','created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class LessonQAAdmin(admin.ModelAdmin):
    list_display = ('lesson','question_no','question','number_answered','number_correct','number_readed','number_shared','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['question']
    exclude = ('number_answered','number_correct','number_readed','number_shared','created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class PrayerTypeAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class PrayerAdmin(admin.ModelAdmin):
    list_display = ('prayer_type','name','number_readed','number_shared','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active','prayer_type',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class CommuintyPrayerAdmin(admin.ModelAdmin):
    list_display = ('gospel','title','created_user','created_on','updated_user','updated_on')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class CeremonyTypeAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['name','name_jp',]
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class CeremonyAdmin(admin.ModelAdmin):
    list_display = ('type','name','number_readed','number_shared','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active','type',)
    search_fields = ['name','name_jp']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user', 'updated_user','updated_on','number_readed','number_shared',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

admin.site.register(YoutubeVideo,YoutubeVideoAdmin)
admin.site.register(Letter,LetterAdmin)
admin.site.register(PostType,PostTypeAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(PostContent,PostContentAdmin)
admin.site.register(Aboutus,AboutusAdmin)
admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(GospelRandom,GospelRandomAdmin)
admin.site.register(Gospel,GospelAdmin)
admin.site.register(GospelContent,GospelContentAdmin)
admin.site.register(GospelReflection,GospelReflectionAdmin)
admin.site.register(MassDateSchedule,MassDateScheduleScheduleAdmin)
admin.site.register(MassTimeSchedule,MassTimeScheduleAdmin)
admin.site.register(ConfessSchedule,ConfessScheduleAdmin)
admin.site.register(LessonType,LessonTypeAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(LessonQA,LessonQAAdmin)
admin.site.register(LessonChapter,LessonChapterAdmin)
admin.site.register(LessonChapterQA,LessonChapterQAAdmin)
admin.site.register(PrayerType,PrayerTypeAdmin)
admin.site.register(Prayer,PrayerAdmin)
admin.site.register(CommuintyPrayer,CommuintyPrayerAdmin)
admin.site.register(CeremonyType,CeremonyTypeAdmin)
admin.site.register(Ceremony,CeremonyAdmin)