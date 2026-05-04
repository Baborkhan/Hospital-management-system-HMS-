from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CommissionTransaction, HospitalAdvertisement, Subscription
from django.db.models import Sum

class CommissionListView(APIView):
    def get(self, request):
        from apps.accounts.views import get_user
        user = get_user(request)
        if not user or user.role not in ("superadmin", "hospital_admin"):
            return Response({"success": False, "message": "Unauthorized"}, status=403)
        qs = CommissionTransaction.objects.all().order_by("-created_at")
        if user.role == "hospital_admin":
            try:
                from apps.hospitals.models import HospitalAdmin as HA
                ha = HA.objects.get(user=user)
                qs = qs.filter(hospital=ha.hospital)
            except Exception:
                qs = qs.none()
        total = float(qs.aggregate(s=Sum("commission_amount"))["s"] or 0)
        return Response({"success": True, "total_commission": total, "count": qs.count(),
                         "data": list(qs.values("source_type","gross_amount","commission_amount",
                                                "status","created_at")[:50])})

class CreateAdvertisementView(APIView):
    def post(self, request):
        from apps.accounts.views import get_user
        from apps.hospitals.models import Hospital
        user = get_user(request)
        if not user or user.role not in ("hospital_admin", "superadmin"):
            return Response({"success": False, "message": "Unauthorized"}, status=403)
        required = ["hospital_id","ad_type","title","total_budget","start_date","end_date"]
        for f in required:
            if not request.data.get(f):
                return Response({"success": False, "message": f"{f} required"}, status=400)
        try:
            hospital = Hospital.objects.get(pk=request.data["hospital_id"])
        except Hospital.DoesNotExist:
            return Response({"success": False, "message": "Hospital not found"}, status=404)
        ad = HospitalAdvertisement.objects.create(
            hospital=hospital, ad_type=request.data["ad_type"],
            title=request.data["title"], total_budget=request.data["total_budget"],
            start_date=request.data["start_date"], end_date=request.data["end_date"],
            description=request.data.get("description",""), status="draft",
        )
        return Response({"success": True, "message": "Advertisement submitted for review",
                         "data": {"id": ad.id, "status": ad.status, "title": ad.title}}, status=201)

urlpatterns = [
    path("commissions/",    CommissionListView.as_view(),      name="commission-list"),
    path("advertisements/", CreateAdvertisementView.as_view(), name="ad-create"),
]
