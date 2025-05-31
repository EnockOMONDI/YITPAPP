from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from . models import Profile,Editpage,SecondSection,SecondSectionIcon,SecondSectionBox,SponsorshipRequest


class EditpageAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'content')  # Display section name and content in the admin list
    search_fields = ['section_name']  # Allow searching by section name for easier management
# Register your models here.
@admin.register(SponsorshipRequest)
class SponsorshipRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_info', 'program_display', 'amount_needed',
        'status_badge', 'financial_situation_display', 'created_at', 'reviewed_at'
    ]
    list_filter = ['status', 'program', 'financial_situation', 'created_at', 'reviewed_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Program Details', {
            'fields': ('program', 'program_other', 'amount_needed')
        }),
        ('Financial Information', {
            'fields': ('financial_situation', 'financial_situation_other', 'reason')
        }),
        ('Supporting Documents', {
            'fields': ('supporting_document',)
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 'emergency_contact_phone',
                'emergency_contact_email', 'emergency_contact_relationship'
            )
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_at', 'admin_notes'),
            'classes': ('collapse',)
        }),
    )

    def user_info(self, obj):
        """Display user information with link to user admin"""
        user_url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}">{}</a><br><small>{}</small>',
            user_url,
            obj.user.get_full_name() or obj.user.username,
            obj.user.email
        )
    user_info.short_description = 'User'
    user_info.admin_order_field = 'user__username'

    def program_display(self, obj):
        """Display program name"""
        return obj.get_program_name()
    program_display.short_description = 'Program'
    program_display.admin_order_field = 'program'

    def financial_situation_display(self, obj):
        """Display financial situation"""
        return obj.get_financial_situation_name()
    financial_situation_display.short_description = 'Financial Situation'
    financial_situation_display.admin_order_field = 'financial_situation'

    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#6c757d',
            'under_review': '#ffc107',
            'approved': '#28a745',
            'rejected': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'reviewed_by')

    def save_model(self, request, obj, form, change):
        """Auto-set reviewed_by and reviewed_at when status changes"""
        if change and 'status' in form.changed_data:
            if obj.status in ['approved', 'rejected']:
                obj.reviewed_by = request.user
                from django.utils import timezone
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

admin.site.register(Profile)
admin.site.register(Editpage, EditpageAdmin)
admin.site.register(SecondSection)
admin.site.register(SecondSectionIcon)
admin.site.register(SecondSectionBox)