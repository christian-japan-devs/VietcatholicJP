from django.contrib import admin

# Register your models here.
from .models import Language, Country, Region, Province, Facility, Church, ChurchImages, Father, FatherAndChurch

class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name','phone','email','region','province')
    list_filter = ('region','province',)
    search_fields = ['name', 'province']

class FatherAdmin(admin.ModelAdmin):
    list_display = ('saint_name','full_name','facility','phone_number', )
    list_filter = ('facility',)
    search_fields = ['full_name', 'facility']

class FatherAndChurchAdmin(admin.ModelAdmin):
    list_display = ('father','church','from_date','to_date','is_active')
    list_filter = ('church',)
    search_fields = ['church', 'father']



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
