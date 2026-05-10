import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

class AdminDashboardView(APIView):
    def get(self, request):
        today = datetime.date.today()
        stats = {}
        try:
            from apps.hospitals.models import Hospital
            from apps.doctors.models import Doctor
            from apps.appointments.models import Appointment
            from apps.accounts.models import User
            stats = {
                "hospitals": {"total": Hospital.objects.count()},
                "doctors": {"total": Doctor.objects.count()},
                "patients": {"total": User.objects.filter(role="patient").count()},
                "appointments": {
                    "total": Appointment.objects.count(),
                    "today": Appointment.objects.filter(appointment_date=today).count(),
                    "pending": Appointment.objects.filter(status="pending").count(),
                },
            }
        except Exception as e:
            stats = {"error": str(e), "note": "Run migrations first"}
        return Response({"success": True, "data": stats})

class SystemHealthView(APIView):
    def get(self, request):
        checks = {}
        try:
            from django.db import connection
            with connection.cursor() as c: c.execute("SELECT 1")
            checks["database"] = "healthy"
        except Exception as e:
            checks["database"] = f"error: {str(e)[:60]}"
        checks["api"] = "healthy"
        overall = "healthy" if checks.get("database") == "healthy" else "degraded"
        return Response({"success": True, "status": overall, "checks": checks,
                         "timestamp": datetime.datetime.now().isoformat(), "version": "1.0.0"})


# ── Audit Log View ─────────────────────────────────────────────────────────────
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class AuditLogView(APIView):
    """Returns last 100 admin audit log entries. Admin only."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Admin access required."}, status=403)
        try:
            from apps.admin_panel.audit_log import AdminAuditLog
            logs = AdminAuditLog.objects.select_related("actor").order_by("-created_at")[:100]
            data = [{
                "id": l.id,
                "actor": l.actor.email if l.actor else "deleted",
                "action": l.action,
                "description": l.description,
                "ip": l.ip_address,
                "time": l.created_at.isoformat(),
            } for l in logs]
            return Response({"success": True, "logs": data})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
