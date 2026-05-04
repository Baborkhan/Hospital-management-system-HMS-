from django.urls import path
from .views import PlatformKPIView, CommissionReportView, AdvertisementReportView, HospitalPerformanceView

urlpatterns = [
    path("kpis/",          PlatformKPIView.as_view(),         name="analytics-kpis"),
    path("commissions/",   CommissionReportView.as_view(),     name="analytics-commissions"),
    path("advertisements/",AdvertisementReportView.as_view(), name="analytics-ads"),
    path("hospitals/",     HospitalPerformanceView.as_view(),  name="analytics-hospitals"),
]
