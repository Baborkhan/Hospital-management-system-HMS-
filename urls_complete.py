"""
MedFind - Complete API URL Configuration
All routes professionally organized and documented
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ── Accounts ──────────────────────────────────────────────────────────────────
from apps.accounts.views import RegisterView, LoginView, ProfileView

# ── Patients ──────────────────────────────────────────────────────────────────
from apps.patients.views import (
    PatientListView, PatientProfileView,
)

# ── Doctors ───────────────────────────────────────────────────────────────────
from apps.doctors.views import DoctorListView, DoctorDetailView

# ── Hospitals ─────────────────────────────────────────────────────────────────
from apps.hospitals.views import HospitalListView, HospitalDetailView, NearbyHospitalsView

# ── Appointments ──────────────────────────────────────────────────────────────
from apps.appointments.views import (
    AppointmentListView, AppointmentDetailView, AvailableSlotsView,
)

# ── Medical Records ───────────────────────────────────────────────────────────
from apps.records.views import MedicalRecordListView, MedicalRecordDetailView

# ── Lab Tests ─────────────────────────────────────────────────────────────────
from apps.labs.views import LabTestListView, LabBookingView, LabBookingDetailView

# ── Pharmacy / Billing ────────────────────────────────────────────────────────
from apps.billing.views import PharmacyProductListView, OrderCreateView, OrderDetailView

# ── Telemedicine ──────────────────────────────────────────────────────────────
from apps.telemedicine.views import (
    TeleconsultSessionCreateView, TeleconsultSessionJoinView,
    TeleconsultSessionEndView, TeleconsultChatMessageView,
    TeleconsultPrescriptionView, TeleconsultSessionHistoryView,
    TeleconsultVerifySessionView,
)

# ── Notifications ─────────────────────────────────────────────────────────────
from apps.notifications.views import NotificationListView, NotificationMarkReadView

# ── Analytics / Admin ─────────────────────────────────────────────────────────
from apps.admin_panel.views import AdminDashboardView, AdminStatsView


# ==============================================================================
# AUTH ROUTES
# ==============================================================================
auth_patterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
]

# ==============================================================================
# PATIENT ROUTES
# ==============================================================================
patient_patterns = [
    path("", PatientListView.as_view(), name="patient-list"),
    path("profile/", PatientProfileView.as_view(), name="patient-profile"),

    # Dashboard — full data bundle
    path("dashboard/", include([
        path("", lambda req: __import__("apps.patients.views",fromlist=["PatientDashboardView"]).PatientDashboardView().get(req), name="patient-dashboard"),
    ])),

    # Medical summary
    path("medical-summary/", include([
        path("", lambda req: __import__("apps.patients.views",fromlist=["PatientMedicalSummaryView"]).PatientMedicalSummaryView().get(req), name="patient-summary"),
    ])),
]

# ==============================================================================
# DOCTOR ROUTES
# ==============================================================================
doctor_patterns = [
    path("", DoctorListView.as_view(), name="doctor-list"),
    path("<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
    path("<int:pk>/schedule/", include([
        # GET /api/v1/doctors/{id}/schedule/?week=0
        path("", lambda req, pk: __import__("apps.doctors.views",fromlist=["DoctorScheduleView"]).DoctorScheduleView().get(req, pk=pk), name="doctor-schedule"),
    ])),
    path("<int:pk>/reviews/", include([
        path("", lambda req, pk: __import__("apps.doctors.views",fromlist=["DoctorReviewsView"]).DoctorReviewsView().get(req, pk=pk), name="doctor-reviews"),
    ])),
]

# ==============================================================================
# HOSPITAL ROUTES
# ==============================================================================
hospital_patterns = [
    path("", HospitalListView.as_view(), name="hospital-list"),
    path("<int:pk>/", HospitalDetailView.as_view(), name="hospital-detail"),
    path("nearby/", NearbyHospitalsView.as_view(), name="hospital-nearby"),
    # GET /api/v1/hospitals/nearby/?lat=23.7&lng=90.4&radius=10
]

# ==============================================================================
# APPOINTMENT ROUTES
# ==============================================================================
appointment_patterns = [
    path("", AppointmentListView.as_view(), name="appointment-list"),
    path("<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),
    path("available-slots/", AvailableSlotsView.as_view(), name="appointment-slots"),
    # GET /api/v1/appointments/available-slots/?doctor=1&date=2025-04-20
]

# ==============================================================================
# MEDICAL RECORD ROUTES
# ==============================================================================
record_patterns = [
    path("", MedicalRecordListView.as_view(), name="record-list"),
    path("<int:pk>/", MedicalRecordDetailView.as_view(), name="record-detail"),

    # PDF export - patient downloads their report
    path("<int:pk>/export-pdf/", include([
        path("", lambda req, pk: __import__("apps.records.views",fromlist=["MedicalRecordPDFExportView"]).MedicalRecordPDFExportView().get(req, pk=pk), name="record-pdf"),
    ])),

    # Download file attachment
    path("<int:pk>/download/", include([
        path("", lambda req, pk: __import__("apps.records.views",fromlist=["RecordDownloadView"]).RecordDownloadView().get(req, pk=pk), name="record-download"),
    ])),

    # Export all records as PDF
    path("export-all/", include([
        path("", lambda req: __import__("apps.records.views",fromlist=["PatientFullRecordExportView"]).PatientFullRecordExportView().get(req), name="record-export-all"),
    ])),

    # Lab report upload (hospital side)
    path("lab-report/upload/", include([
        path("", lambda req: __import__("apps.records.views",fromlist=["LabReportUploadView"]).LabReportUploadView().post(req), name="lab-report-upload"),
    ])),
]

# ==============================================================================
# LAB TEST ROUTES
# ==============================================================================
lab_patterns = [
    path("tests/", LabTestListView.as_view(), name="lab-test-list"),
    path("bookings/", LabBookingView.as_view(), name="lab-booking-list"),
    path("bookings/<int:pk>/", LabBookingDetailView.as_view(), name="lab-booking-detail"),
    # GET /api/v1/labs/tests/?hospital=1&category=blood
    # POST /api/v1/labs/bookings/ → {test, hospital, patient_name, patient_phone, booking_date}
    # PATCH /api/v1/labs/bookings/{id}/ → {status: "completed", result: "..."}
]

# ==============================================================================
# PHARMACY / BILLING ROUTES
# ==============================================================================
billing_patterns = [
    path("products/", PharmacyProductListView.as_view(), name="pharmacy-products"),
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    # POST /api/v1/billing/orders/checkout/
]

# ==============================================================================
# TELEMEDICINE ROUTES
# ==============================================================================
telemedicine_patterns = [
    path("sessions/", TeleconsultSessionCreateView.as_view(), name="tele-session-create"),
    path("sessions/<str:session_id>/join/", TeleconsultSessionJoinView.as_view(), name="tele-session-join"),
    path("sessions/<str:session_id>/end/", TeleconsultSessionEndView.as_view(), name="tele-session-end"),
    path("sessions/<str:session_id>/messages/", TeleconsultChatMessageView.as_view(), name="tele-chat"),
    path("sessions/history/", TeleconsultSessionHistoryView.as_view(), name="tele-history"),
    path("prescriptions/", TeleconsultPrescriptionView.as_view(), name="tele-prescription"),
    path("verify-session/", TeleconsultVerifySessionView.as_view(), name="tele-verify"),
]

# ==============================================================================
# NOTIFICATION ROUTES
# ==============================================================================
notification_patterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<int:pk>/read/", NotificationMarkReadView.as_view(), name="notification-read"),
]

# ==============================================================================
# ADMIN / ANALYTICS ROUTES
# ==============================================================================
admin_patterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("stats/", AdminStatsView.as_view(), name="admin-stats"),
]

# ==============================================================================
# LOCATION ROUTES (for ViewMaps)
# ==============================================================================
location_patterns = [
    path("nearby/", NearbyHospitalsView.as_view(), name="location-nearby"),
    # GET /api/v1/locations/nearby/?lat=23.7&lng=90.4&radius=10&type=hospital
]

# ==============================================================================
# MASTER URL CONF — API v1
# ==============================================================================
api_v1_patterns = [
    path("auth/", include(auth_patterns)),
    path("patients/", include(patient_patterns)),
    path("doctors/", include(doctor_patterns)),
    path("hospitals/", include(hospital_patterns)),
    path("appointments/", include(appointment_patterns)),
    path("records/", include(record_patterns)),
    path("labs/", include(lab_patterns)),
    path("billing/", include(billing_patterns)),
    path("telemedicine/", include(telemedicine_patterns)),
    path("notifications/", include(notification_patterns)),
    path("admin/", include(admin_patterns)),
    path("locations/", include(location_patterns)),
]

urlpatterns = [
    path("api/v1/", include(api_v1_patterns)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

