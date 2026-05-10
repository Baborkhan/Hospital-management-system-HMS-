from django.contrib import admin
from .models import EmailOTP


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display  = ('email', 'otp', 'created_at', 'expires_at', 'is_used', 'attempt_count')
    list_filter   = ('is_used',)
    search_fields = ('email',)
    readonly_fields = ('created_at', 'expires_at', 'attempt_count')
    ordering = ('-created_at',)

