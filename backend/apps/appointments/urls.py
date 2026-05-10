from django.urls import path
from .views import AppointmentListView, AppointmentDetailView, AvailableSlotsView

urlpatterns = [
    path("",               AppointmentListView.as_view(),  name="appointment-list"),
    path("<int:pk>/",      AppointmentDetailView.as_view(), name="appointment-detail"),
    path("slots/",         AvailableSlotsView.as_view(),   name="available-slots"),
]
