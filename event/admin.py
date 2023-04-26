from django.contrib import admin
from django.utils import timezone
from .models import (Event,EventProgramDetail,EventRuleContent,Registration,
            EventBoard,EventBoardAndMember,EventBoardTask,EventGroup,UserAndEventGroup,EventGroupScoreType,EventGroupScore,
            EventTransactionAccount,EventTransaction,RegistrationTemp)

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('name','title','event_date','event_fee','number_of_registered_ticket','number_of_confirmed_ticket','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active','province',)
    search_fields = ['name', 'excerpt',]
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('number_of_registered_ticket','number_of_confirmed_ticket','created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventProgramDetailAdmin(admin.ModelAdmin):
    list_display = ('event','title','event_date','from_time','to_time','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title']
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventRuleContentAdmin(admin.ModelAdmin):
    list_display = ('event','title','sequence','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('date_time','user','event','payment_status','confirm_status','updated_user','updated_on')
    list_filter = ('event',)
    search_fields = ['user']
    exclude = ('updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventBoardAdmin(admin.ModelAdmin):
    list_display = ('event','title','facebook_link','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventBoardAndMemberAdmin(admin.ModelAdmin):
    list_display = ('event_board','member','member_type','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventBoardTaskAdmin(admin.ModelAdmin):
    list_display = ('board','title','status','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventGroupAdmin(admin.ModelAdmin):
    list_display = ('event','name','facebook_link','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class UserAndEventGroupAdmin(admin.ModelAdmin):
    list_display = ('event_group','member','member_type','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventGroupScoreTypeAdmin(admin.ModelAdmin):
    list_display = ('title','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventGroupScoreAdmin(admin.ModelAdmin):
    list_display = ('event_group','date','on_account','score_amount','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventTransactionAccountAdmin(admin.ModelAdmin):
    list_display = ('title','is_active','created_user','created_on','updated_user','updated_on')
    list_filter = ('is_active',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class EventTransactionAdmin(admin.ModelAdmin):
    list_display = ('event','date','transaction_type','transaction_amount','on_account','created_user','created_on','updated_user','updated_on')
    list_filter = ('on_account','transaction_type',)
    exclude = ('created_on','created_user','updated_user','updated_on',)
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

class RegistrationTempAdmin(admin.ModelAdmin):
    list_display = ('email','full_name','team_no','status','present_status','payment_code','ticket_code','updated_user')
    list_filter = ('status','team_no','present_status','province')
    search_fields = ['full_name','email','payment_code','ticket_code']
    exclude = ('updated_user','status','payment_code','ticket_code','present_status','updated_on')
    list_per_page = 30

    def save_model(self, request, obj, form, change):
        obj.updated_on = timezone.now
        obj.updated_user = request.user
        obj.save()

admin.site.register(Event,EventAdmin)
admin.site.register(EventProgramDetail,EventProgramDetailAdmin)
admin.site.register(EventRuleContent,EventRuleContentAdmin)
admin.site.register(Registration,RegistrationAdmin)
admin.site.register(EventBoard,EventBoardAdmin)
admin.site.register(EventBoardAndMember,EventBoardAndMemberAdmin)
admin.site.register(EventBoardTask,EventBoardTaskAdmin)
admin.site.register(EventGroup,EventGroupAdmin)
admin.site.register(UserAndEventGroup,UserAndEventGroupAdmin)
admin.site.register(EventGroupScoreType,EventGroupScoreTypeAdmin)
admin.site.register(EventGroupScore,EventGroupScoreAdmin)
admin.site.register(EventTransactionAccount,EventTransactionAccountAdmin)
admin.site.register(EventTransaction,EventTransactionAdmin)
admin.site.register(RegistrationTemp,RegistrationTempAdmin)