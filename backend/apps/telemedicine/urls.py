from django.urls import path
from .views import (
    TeleconsultSessionCreateView, TeleconsultSessionJoinView,
    TeleconsultSessionEndView, TeleconsultChatMessageView,
    TeleconsultPrescriptionView, TeleconsultSessionHistoryView,
    TeleconsultVerifySessionView,
    PatientJoinWaitingRoomView, DoctorJoinSessionView,
)

urlpatterns = [
    # Session lifecycle
    path("sessions/",                                TeleconsultSessionCreateView.as_view(),   name="session-create"),
    path("sessions/<str:room_id>/verify/",           TeleconsultVerifySessionView.as_view(),   name="session-verify"),

    # Spec §1 — Waiting room & doctor join
    path("sessions/<str:session_id>/patient-join/",  PatientJoinWaitingRoomView.as_view(),     name="patient-join-waiting"),
    path("sessions/<str:session_id>/doctor-join/",   DoctorJoinSessionView.as_view(),          name="doctor-join-session"),

    # Legacy join (generic)
    path("sessions/<str:room_id>/join/",             TeleconsultSessionJoinView.as_view(),     name="session-join"),
    path("sessions/<str:room_id>/end/",              TeleconsultSessionEndView.as_view(),      name="session-end"),

    # In-session
    path("sessions/<str:room_id>/chat/",             TeleconsultChatMessageView.as_view(),     name="session-chat"),
    path("sessions/<str:room_id>/prescription/",     TeleconsultPrescriptionView.as_view(),    name="session-rx"),

    # History
    path("history/",                                 TeleconsultSessionHistoryView.as_view(),  name="session-history"),
]
