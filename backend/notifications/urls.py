from django.urls import path
from .views import NotificationListView

urlpatterns = [
    path("",          NotificationListView.as_view(), name="notifications"),
    path("mark-read/",NotificationListView.as_view(), name="notif-mark-read"),
]
