from django.urls import path
from .views import InvoiceListView, InvoiceDetailView
urlpatterns = [
    path("invoices/", InvoiceListView.as_view()),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view()),
]
