from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_joined', 'is_active')
    list_filter = ('gender', 'is_active', 'districts', 'farmer_groups')
    search_fields = ('agent_id', 'first_name', 'last_name', 'email', 'phone_number')
    filter_horizontal = ('districts', 'farmer_groups')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('agent_id', 'first_name', 'last_name', 'email', 'phone_number', 'gender')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'date_joined', 'farmers_profiled')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Associations', {
            'fields': ('districts', 'farmer_groups')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
