from django.contrib import admin

# Register your models here.
from .models import Language, Country, Region, Province, Facility, Church, ChurchImages, Father, FatherAndChurch,Community

class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name','phone','email','province')
    list_filter = ('region','province',)
    search_fields = ['name', 'province']

class FatherAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number', )
    list_filter = ('province',)
    search_fields = ['introduction']

class FatherAndChurchAdmin(admin.ModelAdmin):
    list_display = ('father','church','from_date','to_date','is_active')
    list_filter = ('church',)
    search_fields = ['church', 'father']

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name','type','province','address')
    list_filter = ('province',)
    search_fields = ['name', 'address']
    prepopulated_fields = {'slug': ('name',)}

# Register your models here. 
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Facility)
admin.site.register(Church,ChurchAdmin)
admin.site.register(ChurchImages)
admin.site.register(Father, FatherAdmin)
admin.site.register(FatherAndChurch,FatherAndChurchAdmin)
admin.site.register(Community,CommunityAdmin)