from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import (Language, Country, Region, Province, 
        Facility, Church, ChurchImages, Father, FatherAndChurch,Community,
        RepresentativeResponsibility, Representative, RepresentativeAndCommunity
        ,UserProfile,ContactUs)

class FacilityAdmin(admin.ModelAdmin):
    list_display = ('kanji','name','phone','email','province','created_on','created_user', 'updated_user')
    list_filter = ('region','province',)
    search_fields = ['name', 'kanji']
    exclude = ('created_on','created_user','updated_on','updated_user',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name','phone','email','province','created_on','created_user', 'updated_user')
    list_filter = ('region','province',)
    search_fields = ['name', 'province']
    exclude = ('created_on','created_user','updated_on','updated_user',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class ChurchImagesAdmin(admin.ModelAdmin):
    list_display = ('title','church','created_user', 'created_on')
    list_filter = ('church',)
    search_fields = ['title']
    exclude = ('created_on','created_user')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class FatherAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number','created_on','created_user', 'updated_user')
    list_filter = ('province',)
    search_fields = ['introduction']
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class FatherAndChurchAdmin(admin.ModelAdmin):
    list_display = ('father','church','from_date','to_date','is_active','created_on','created_user', 'updated_user')
    list_filter = ('church',)
    search_fields = ['church', 'father']
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name','type','province','address','created_on','created_user', 'updated_user')
    list_filter = ('province',)
    search_fields = ['name', 'address']
    exclude = ('created_on','created_user', 'updated_user','updated_on',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class RepresentativeResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('name','updated_on','updated_user','created_on','created_user', 'updated_user')
    list_filter = ('is_active',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_user', 'updated_user',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('user','facebook','province','phone_number','updated_user','created_on','created_user', 'updated_user')
    list_filter = ('province',)
    search_fields = ['user', 'facebook']
    exclude = ('created_user', 'updated_user',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class RepresentativeAndCommunityAdmin(admin.ModelAdmin):
    list_display = ('representative','responsibility','community','from_date','to_date','created_on','created_user', 'updated_user')
    list_filter = ('is_active','community',)
    search_fields = ['community', 'representative']
    exclude = ('created_user', 'updated_user',)
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','facebook','province','community','phone_number')
    list_filter = ('is_active','province','community')
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name','email','province','question','is_replied','created_on','updated_user','updated_on')
    list_filter = ('is_replied','province')
    exclude = ('is_replied','created_on','updated_on', 'updated_user',)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

# Register your models here. 
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Facility,FacilityAdmin)
admin.site.register(Church,ChurchAdmin)
admin.site.register(ChurchImages,ChurchImagesAdmin)
admin.site.register(Father, FatherAdmin)
admin.site.register(FatherAndChurch,FatherAndChurchAdmin)
admin.site.register(Community,CommunityAdmin)
admin.site.register(RepresentativeResponsibility,RepresentativeResponsibilityAdmin)
admin.site.register(Representative,RepresentativeAdmin)
admin.site.register(RepresentativeAndCommunity,RepresentativeAndCommunityAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(ContactUs,ContactUsAdmin)