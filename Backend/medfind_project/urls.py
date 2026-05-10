# medfind/medfind_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
from django.http import JsonResponse


def health_check(request):
    """Render health check + API status endpoint."""
    return JsonResponse({
        "status": "ok",
        "service": "MedFind Bangladesh API",
        "version": "3.0",
        "ai": "gemini" if getattr(settings, "GEMINI_API_KEY", "") else "unconfigured",
    })


urlpatterns = [
    # ── Health / Root ─────────────────────────────────────────
    path('',               health_check, name='health'),
    path('api/v1/health/', health_check, name='health-v1'),

    # ── Django Admin ──────────────────────────────────────────
    path('admin/',         admin.site.urls),

    # ── AI endpoints ─────────────────────────────────────────
    # /api/v1/ai/chat/  ← frontend uses this
=======
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/',         admin.site.urls),

    # ── AI endpoints ─────────────────────────────────────────
    # /api/v1/ai/chat/  ← frontend uses this (MEDFIND_CONFIG.API_BASE + /ai/chat/)
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
    path('api/v1/ai/',     include('ai.urls')),
    # /api/ai/chat/  ← legacy path (kept for compatibility)
    path('api/ai/',        include('ai.urls')),

    # ── OTP Authentication ───────────────────────────────────
<<<<<<< HEAD
    path('api/v1/accounts/', include('otp_auth.urls')),

    # ── Donate / Blood Bank ──────────────────────────────────
    path('api/donate/',    include('donate.urls')),
    path('api/v1/donate/', include('donate.urls')),

=======
    # Matches frontend fetch calls:  API + '/accounts/send-login-otp/'
    path('api/v1/accounts/', include('otp_auth.urls')),

    # ── Donate ──────────────────────────────────────────────
    path('api/donate/',    include('donate.urls')),
    path('api/v1/donate/', include('donate.urls')),

    # ── Frontend (serve at root) ─────────────────────────────
    path('',               TemplateView.as_view(template_name='index.html'), name='home'),
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

