from django.urls import path
from .views import AdminDashboardView, SystemHealthView
urlpatterns = [
    path("", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("health/", SystemHealthView.as_view(), name="system-health"),
]
