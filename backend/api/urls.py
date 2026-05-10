from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_user, name='api-register'),
    path('auth/login/', views.login_user, name='api-login'),
    path('auth/logout/', views.logout_user, name='api-logout'),
    path('patients/', views.patient_list, name='api-patient-list'),
    path('patients/<int:pk>/', views.patient_detail, name='api-patient-detail'),
    path('doctors/', views.doctor_list, name='api-doctor-list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='api-doctor-detail'),
    path('appointments/', views.appointment_list, name='api-appointment-list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='api-appointment-detail'),
    path('admissions/', views.admission_list, name='api-admission-list'),
    path('admissions/<int:pk>/', views.admission_detail, name='api-admission-detail'),
    path('bills/', views.bill_list, name='api-bill-list'),
    path('bills/<int:pk>/', views.bill_detail, name='api-bill-detail'),
]
