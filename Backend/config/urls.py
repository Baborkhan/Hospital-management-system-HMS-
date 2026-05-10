from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({"status": "ok", "message": "MedFind API is running"})

urlpatterns = [
    path("", api_root),                                          # ← এটা যোগ করো
    path("admin/", admin.site.urls),
    path("api/v1/", include("config.api.v1_urls")),
    path("api/donate/", include("donate.urls")),
]
