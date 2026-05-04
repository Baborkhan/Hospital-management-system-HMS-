from django.urls import path
from .views import DoctorListView, DoctorDetailView
urlpatterns = [
    path("", DoctorListView.as_view()),
    path("<int:pk>/", DoctorDetailView.as_view()),
]
