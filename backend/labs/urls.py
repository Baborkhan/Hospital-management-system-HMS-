from django.urls import path
from .views import LabTestListView, LabBookingView, LabBookingDetailView
urlpatterns = [
    path("tests/", LabTestListView.as_view()),
    path("bookings/", LabBookingView.as_view()),
    path("bookings/<int:pk>/", LabBookingDetailView.as_view()),
]
