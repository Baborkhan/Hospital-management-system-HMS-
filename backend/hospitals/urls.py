from django.urls import path
from .views import HospitalListView, HospitalDetailView, NearbyHospitalsView, HospitalBedAvailabilityView

urlpatterns = [
    path("",                         HospitalListView.as_view(),          name="hospital-list"),
    path("<int:pk>/",                HospitalDetailView.as_view(),         name="hospital-detail"),
    path("nearby/",                  NearbyHospitalsView.as_view(),        name="hospital-nearby"),
    path("<int:pk>/availability/",   HospitalBedAvailabilityView.as_view(),name="hospital-availability"),
]
