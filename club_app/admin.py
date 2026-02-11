from django.contrib import admin
from .models import News, MembershipRequest, ClubSettings
from django.utils.html import format_html

# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'content')

@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'mobile', 'email')
    actions = ['approve_requests', 'reject_requests']
    readonly_fields = ('aadhaar_display',)

    def aadhaar_display(self, obj):
        # Decrypt Aadhaar for display in Admin
        return obj.get_aadhaar()
    aadhaar_display.short_description = "Aadhaar Number"

    def approve_requests(self, request, queryset):
        queryset.update(status='Approved')
    approve_requests.short_description = "Approve selected requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
    reject_requests.short_description = "Reject selected requests"

@admin.register(ClubSettings)
class ClubSettingsAdmin(admin.ModelAdmin):
    pass
