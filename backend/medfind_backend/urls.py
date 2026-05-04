"""
URL Configuration for medfind_backend project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'hospitals', views.HospitalViewSet, basename='hospital')
router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'lab-tests', views.LabTestViewSet, basename='lab-test')
router.register(r'billing', views.BillingViewSet, basename='billing')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('api.urls')),
    path('api/donation/', include('donation.urls')),
]
