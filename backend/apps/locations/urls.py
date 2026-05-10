from django.urls import path
from .views import DivisionListView
urlpatterns = [path("divisions/", DivisionListView.as_view())]
