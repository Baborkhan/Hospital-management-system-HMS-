# medfind/ai/urls.py
from django.urls import path
from .views import AIChatView, SymptomAnalyzeView, ChatHistoryView, HealthRecordView, ProxyAIChatView

urlpatterns = [
    # ── Proxy endpoint (frontend sends full Anthropic payload, backend adds key) ──
    path('chat/',         ProxyAIChatView.as_view(),    name='ai-proxy-chat'),

    # ── Legacy endpoints ──
    path('chat/legacy/',  AIChatView.as_view(),         name='ai-chat'),
    path('symptoms/',     SymptomAnalyzeView.as_view(), name='ai-symptoms'),
    path('history/',      ChatHistoryView.as_view(),    name='ai-history'),
    path('health/',       HealthRecordView.as_view(),   name='health-record'),
]

