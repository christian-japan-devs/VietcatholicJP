from django.contrib import admin

# Register your models here.
from .models import YoutubeVideo,Letter, PostType,Post,PostContent,Aboutus,Announcement,Gospel,GospelContent,GospelReflection, MassDateSchedule, MassTimeSchedule, ConfessSchedule

class LetterAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'isActive','created_on')
    list_filter = ('isActive',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','isActive','created_on')
    list_filter = ('isActive',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class PostContentAdmin(admin.ModelAdmin):
    list_display = ('chapter_title','slug','created_on')
    list_filter = ('post',)
    search_fields = ['chapter_title', 'content']
    prepopulated_fields = {'slug': ('chapter_title',)}

class AboutusAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'isActive','created_on')
    list_filter = ('isActive',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_on')
    list_filter = ('isActive',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class GospelAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class GospelContentAdmin(admin.ModelAdmin):
    list_display = ('chapter_title','slug','created_on')
    search_fields = ['chapter_title', 'content','chapter_reference']
    prepopulated_fields = {'slug': ('chapter_title',)}

class GospelReflectionAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_on')
    search_fields = ['title', 'content','chapter_reference']
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
admin.site.register(MassDateSchedule)
admin.site.register(MassTimeSchedule,MassTimeScheduleAdmin)
admin.site.register(ConfessSchedule,ConfessScheduleAdmin)