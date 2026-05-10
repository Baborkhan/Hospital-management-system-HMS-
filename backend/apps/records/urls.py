from django.urls import path
from .views import (
    MedicalRecordListView, MedicalRecordDetailView,
    MedicalRecordPDFExportView, PatientFullRecordExportView,
    LabReportUploadView, RecordDownloadView,
)

urlpatterns = [
    path("",                          MedicalRecordListView.as_view(),       name="records"),
    path("<int:pk>/",                 MedicalRecordDetailView.as_view(),     name="record-detail"),
    path("<int:pk>/pdf/",             MedicalRecordPDFExportView.as_view(),  name="record-pdf"),
    path("export/full/",              PatientFullRecordExportView.as_view(), name="record-full-export"),
    path("lab-reports/upload/",       LabReportUploadView.as_view(),         name="lab-upload"),
    path("download/<int:pk>/",        RecordDownloadView.as_view(),          name="record-download"),
]
