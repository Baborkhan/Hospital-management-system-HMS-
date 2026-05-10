from django.urls import path
from .views import MedicineListView, PharmacyOrderView, PharmacyOrderDetailView
urlpatterns = [
    path("medicines/", MedicineListView.as_view()),
    path("orders/", PharmacyOrderView.as_view()),
    path("orders/<int:pk>/", PharmacyOrderDetailView.as_view()),
]
