from django.urls import path
from .views import PatientListView, PatientProfileView, PatientDashboardView, PatientMedicalSummaryView

urlpatterns = [
    path("",                 PatientListView.as_view(),          name="patient-list"),
    path("profile/",         PatientProfileView.as_view(),        name="patient-profile"),
    path("dashboard/",       PatientDashboardView.as_view(),      name="patient-dashboard"),
    path("medical-summary/", PatientMedicalSummaryView.as_view(), name="patient-medical-summary"),
]
