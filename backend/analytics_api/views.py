"""
MedFind Analytics API — Powered by Pandas + NumPy
Provides KPIs, charts, forecasting, commission reports
API: /api/v1/analytics/
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Avg, Q
from datetime import timedelta
import logging

try:
    import pandas as pd
    import numpy as np
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

logger = logging.getLogger(__name__)


def get_user(request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "): return None
    try:
        from apps.accounts.models import User
        uid = int(auth.replace("Bearer ", "").split("_")[2])
        return User.objects.get(pk=uid, is_active=True)
    except Exception:
        return None


class PlatformKPIView(APIView):
    """
    GET /api/v1/analytics/kpis/
    Platform-wide KPIs — pandas-computed with rolling averages.
    """
    def get(self, request):
        user = get_user(request)
        if not user or user.role not in ("superadmin", "hospital_admin"):
            return Response({"success": False, "message": "Admin access required"}, status=403)

        now   = timezone.now()
        today = now.date()
        week_ago  = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # ─── Live counts ───────────────────────────────────────────
        try:
            from apps.hospitals.models import Hospital
            from apps.doctors.models import Doctor
            from apps.patients.models import Patient
            from apps.appointments.models import Appointment
            from apps.pharmacy.models import PharmacyOrder
            from apps.labs.models import LabBooking
            from apps.monetization.models import CommissionTransaction, HospitalAdvertisement

            total_hospitals  = Hospital.objects.filter(is_active=True).count()
            total_doctors    = Doctor.objects.filter(is_verified=True).count()
            total_patients   = Patient.objects.count()
            total_appts      = Appointment.objects.count()
            appts_today      = Appointment.objects.filter(appointment_date=today).count()
            appts_this_week  = Appointment.objects.filter(appointment_date__gte=week_ago).count()

            # Commission stats
            comm_qs = CommissionTransaction.objects.all()
            total_commission    = float(comm_qs.aggregate(s=Sum("commission_amount"))["s"] or 0)
            this_month_comm     = float(comm_qs.filter(created_at__date__gte=month_ago)
                                         .aggregate(s=Sum("commission_amount"))["s"] or 0)
            pending_commission  = float(comm_qs.filter(status="pending")
                                         .aggregate(s=Sum("commission_amount"))["s"] or 0)

            # Ad revenue
            ad_revenue = float(HospitalAdvertisement.objects.filter(status="active")
                               .aggregate(s=Sum("amount_spent"))["s"] or 0)
            active_ads = HospitalAdvertisement.objects.filter(status="active").count()

            # Pharmacy
            pharm_revenue = float(PharmacyOrder.objects.filter(status="delivered")
                                   .aggregate(s=Sum("total"))["s"] or 0)

            # ─── Pandas analysis on appointments ───────────────────
            pandas_stats = {}
            if PANDAS_OK:
                appt_data = list(Appointment.objects.values(
                    "appointment_date", "status", "fee"
                ).order_by("appointment_date"))

                if appt_data:
                    df = pd.DataFrame(appt_data)
                    df["appointment_date"] = pd.to_datetime(df["appointment_date"])
                    df["fee"] = pd.to_numeric(df["fee"], errors="coerce").fillna(0)

                    # Completion rate
                    completion_rate = round(
                        len(df[df["status"] == "completed"]) / len(df) * 100, 1
                    ) if len(df) > 0 else 0

                    # 7-day appointment rolling trend
                    daily = df.groupby("appointment_date").size().reset_index(name="count")
                    daily["rolling_7d"] = daily["count"].rolling(7, min_periods=1).mean().round(1)

                    # Revenue statistics
                    completed_df = df[df["status"] == "completed"]
                    avg_fee      = float(np.mean(completed_df["fee"].values)) if len(completed_df) > 0 else 0
                    std_fee      = float(np.std(completed_df["fee"].values)) if len(completed_df) > 0 else 0
                    total_rev    = float(np.sum(completed_df["fee"].values))

                    # Weekly trend last 4 weeks
                    weekly = df.copy()
                    weekly["week"] = weekly["appointment_date"].dt.isocalendar().week
                    weekly_counts = weekly.groupby("week").size().tail(4).tolist()

                    pandas_stats = {
                        "completion_rate": completion_rate,
                        "avg_fee": round(avg_fee, 2),
                        "std_fee": round(std_fee, 2),
                        "total_appointment_revenue": round(total_rev, 2),
                        "weekly_trend": weekly_counts,
                        "rolling_7d_avg": float(daily["rolling_7d"].iloc[-1]) if len(daily) > 0 else 0,
                    }

            total_revenue = total_commission + ad_revenue + pharm_revenue * 0.05  # 5% on pharmacy

            return Response({
                "success": True,
                "computed_with": "pandas+numpy" if PANDAS_OK else "raw_django_orm",
                "data": {
                    "overview": {
                        "total_hospitals":  total_hospitals,
                        "total_doctors":    total_doctors,
                        "total_patients":   total_patients,
                        "total_appointments": total_appts,
                        "appointments_today": appts_today,
                        "appointments_this_week": appts_this_week,
                    },
                    "revenue": {
                        "total_commission":   round(total_commission, 2),
                        "this_month_commission": round(this_month_comm, 2),
                        "pending_commission": round(pending_commission, 2),
                        "ad_revenue":         round(ad_revenue, 2),
                        "pharmacy_revenue":   round(pharm_revenue, 2),
                        "total_platform_revenue": round(total_revenue, 2),
                        "active_ads":         active_ads,
                    },
                    "analytics": pandas_stats,
                    "generated_at": now.isoformat(),
                }
            })

        except Exception as e:
            logger.error(f"KPI compute error: {e}")
            return Response({"success": False, "message": str(e)}, status=500)


class CommissionReportView(APIView):
    """
    GET /api/v1/analytics/commissions/
    Commission breakdown by hospital, source_type, date range.
    """
    def get(self, request):
        user = get_user(request)
        if not user or user.role != "superadmin":
            return Response({"success": False, "message": "Superadmin only"}, status=403)

        from apps.monetization.models import CommissionTransaction

        days = int(request.query_params.get("days", 30))
        since = timezone.now().date() - timedelta(days=days)
        qs = CommissionTransaction.objects.filter(created_at__date__gte=since)

        if PANDAS_OK:
            data = list(qs.values("source_type", "commission_amount", "gross_amount",
                                  "hospital__name", "created_at", "status"))
            if data:
                df = pd.DataFrame(data)
                df["commission_amount"] = pd.to_numeric(df["commission_amount"], errors="coerce")
                df["gross_amount"]      = pd.to_numeric(df["gross_amount"], errors="coerce")
                df["created_at"]        = pd.to_datetime(df["created_at"]).dt.date

                by_type = df.groupby("source_type").agg(
                    total_commission=("commission_amount", "sum"),
                    count=("commission_amount", "count"),
                    avg_gross=("gross_amount", "mean"),
                ).round(2).reset_index().to_dict(orient="records")

                by_hospital = df.groupby("hospital__name").agg(
                    total_commission=("commission_amount", "sum"),
                    count=("commission_amount", "count"),
                ).round(2).reset_index().sort_values("total_commission", ascending=False
                ).head(10).to_dict(orient="records")

                daily_trend = df.groupby("created_at")["commission_amount"].sum().reset_index()
                daily_trend.columns = ["date", "amount"]
                daily_trend["date"] = daily_trend["date"].astype(str)

                total = float(df["commission_amount"].sum())
                avg   = float(np.mean(df["commission_amount"].values))
                std   = float(np.std(df["commission_amount"].values))

                return Response({
                    "success": True,
                    "period_days": days,
                    "summary": {"total": round(total,2), "mean": round(avg,2), "std": round(std,2), "count": len(df)},
                    "by_type": by_type,
                    "top_hospitals": by_hospital,
                    "daily_trend": daily_trend.to_dict(orient="records"),
                })

        # Fallback without pandas
        total = float(qs.aggregate(s=Sum("commission_amount"))["s"] or 0)
        return Response({"success": True, "total": total, "count": qs.count()})


class AdvertisementReportView(APIView):
    """
    GET /api/v1/analytics/advertisements/
    Ad revenue tracking and CTR analysis.
    """
    def get(self, request):
        user = get_user(request)
        if not user or user.role != "superadmin":
            return Response({"success": False, "message": "Superadmin only"}, status=403)

        from apps.monetization.models import HospitalAdvertisement

        ads = list(HospitalAdvertisement.objects.select_related("hospital").values(
            "hospital__name", "ad_type", "total_budget", "amount_spent",
            "impressions", "clicks", "status"
        ))

        if PANDAS_OK and ads:
            df = pd.DataFrame(ads)
            df["total_budget"]  = pd.to_numeric(df["total_budget"], errors="coerce")
            df["amount_spent"]  = pd.to_numeric(df["amount_spent"], errors="coerce")
            df["ctr"] = (df["clicks"] / df["impressions"].replace(0, np.nan) * 100).round(2).fillna(0)

            total_revenue = float(df["amount_spent"].sum())
            avg_ctr       = float(df["ctr"].mean())

            by_type = df.groupby("ad_type").agg(
                revenue=("amount_spent", "sum"),
                impressions=("impressions", "sum"),
                clicks=("clicks", "sum"),
            ).round(2).reset_index().to_dict(orient="records")

            return Response({
                "success": True,
                "summary": {
                    "total_ad_revenue": round(total_revenue, 2),
                    "avg_ctr": round(avg_ctr, 2),
                    "total_ads": len(df),
                    "active_ads": int(df[df["status"]=="active"].shape[0]),
                },
                "by_type": by_type,
                "ads": df.head(20).to_dict(orient="records"),
            })

        return Response({"success": True, "total_ads": len(ads)})


class HospitalPerformanceView(APIView):
    """
    GET /api/v1/analytics/hospitals/
    Per-hospital KPIs using pandas aggregation.
    """
    def get(self, request):
        user = get_user(request)
        if not user or user.role not in ("superadmin", "hospital_admin"):
            return Response({"success": False, "message": "Admin required"}, status=403)

        from apps.hospitals.models import Hospital
        from apps.appointments.models import Appointment
        from apps.monetization.models import CommissionTransaction

        hospitals = Hospital.objects.filter(is_active=True)
        results = []

        for h in hospitals[:20]:  # Top 20 for performance
            appt_count   = Appointment.objects.filter(hospital=h).count()
            commission   = float(CommissionTransaction.objects.filter(hospital=h)
                                 .aggregate(s=Sum("commission_amount"))["s"] or 0)
            occupancy    = round((h.total_beds - h.available_beds) / h.total_beds * 100, 1) \
                           if h.total_beds > 0 else 0
            results.append({
                "hospital":      h.name,
                "division":      h.division,
                "rating":        float(h.rating),
                "beds":          h.total_beds,
                "occupancy_pct": occupancy,
                "appointments":  appt_count,
                "commission_paid": round(commission, 2),
                "is_premium":    getattr(h, "is_premium", False),
            })

        if PANDAS_OK and results:
            df = pd.DataFrame(results)
            df = df.sort_values("commission_paid", ascending=False)
            # Numpy stats
            occ_mean = float(np.mean(df["occupancy_pct"].values))
            occ_std  = float(np.std(df["occupancy_pct"].values))
            return Response({
                "success": True,
                "summary": {
                    "avg_occupancy": round(occ_mean, 1),
                    "std_occupancy": round(occ_std, 1),
                    "total_commission_generated": round(float(df["commission_paid"].sum()), 2),
                },
                "hospitals": df.to_dict(orient="records"),
            })

        return Response({"success": True, "hospitals": results})
