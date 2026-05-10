# medfind/ai/admin.py
from django.contrib import admin
from .models import ChatSession, ChatMessage, HealthRecord


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display  = ['session_id', 'user_id', 'user_ip', 'language', 'turn_count', 'created_at']
    list_filter   = ['language', 'created_at']
    search_fields = ['session_id', 'user_id', 'user_ip']
    ordering      = ['-created_at']
    readonly_fields = ['session_id', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display  = ['session', 'role', 'urgency', 'specialist', 'is_emergency', 'created_at']
    list_filter   = ['role', 'is_emergency', 'urgency', 'created_at']
    search_fields = ['content', 'specialist']
    ordering      = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display  = ['user_id', 'bmi', 'systolic', 'diastolic', 'sugar', 'weight', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['user_id']
    ordering      = ['-created_at']




