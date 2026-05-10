"""
MedFind Monetization:
  1. CommissionTransaction — 5%+ per appointment/lab booking
  2. HospitalAdvertisement — hospitals pay to advertise on platform
  3. Subscription — hospital platform subscription plans
"""
from django.db import models
from django.utils import timezone


class CommissionTransaction(models.Model):
    """5% platform commission on every booking."""
    SOURCE_TYPES = [
        ("appointment", "Appointment"),
        ("lab_booking",  "Lab Booking"),
        ("pharmacy",     "Pharmacy Order"),
    ]
    STATUS = [
        ("pending",   "Pending"),
        ("collected", "Collected"),
        ("disputed",  "Disputed"),
        ("refunded",  "Refunded"),
    ]
    hospital      = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE,
                                      related_name="commissions", db_index=True)
    source_type   = models.CharField(max_length=15, choices=SOURCE_TYPES, db_index=True)
    source_ref    = models.CharField(max_length=50)   # appointment_id / booking_id / order_id
    gross_amount  = models.DecimalField(max_digits=10, decimal_places=2)  # Full transaction
    commission_rate  = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)  # 5%
    commission_amount= models.DecimalField(max_digits=10, decimal_places=2)  # Gross × rate/100
    hospital_payout  = models.DecimalField(max_digits=10, decimal_places=2)  # Gross − commission
    status        = models.CharField(max_length=10, choices=STATUS, default="pending", db_index=True)
    collected_at  = models.DateTimeField(null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "mf_commission_transactions"
        ordering = ["-created_at"]
        indexes  = [
            models.Index(fields=["hospital", "status"]),
            models.Index(fields=["source_type", "created_at"]),
        ]

    def save(self, *args, **kwargs):
        self.commission_amount = round(float(self.gross_amount) * float(self.commission_rate) / 100, 2)
        self.hospital_payout   = round(float(self.gross_amount) - float(self.commission_amount), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commission ৳{self.commission_amount} from {self.hospital} [{self.source_type}]"


class HospitalAdvertisement(models.Model):
    """Hospital pays MedFind to advertise — banner / featured listing / sponsored."""
    AD_TYPES = [
        ("featured_listing", "Featured Hospital Listing"),
        ("homepage_banner",  "Homepage Banner"),
        ("search_boost",     "Search Boost"),
        ("category_sponsor", "Category Sponsor"),
    ]
    STATUS = [
        ("draft",    "Draft"),
        ("active",   "Active"),
        ("paused",   "Paused"),
        ("expired",  "Expired"),
        ("rejected", "Rejected"),
    ]
    hospital      = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE,
                                      related_name="advertisements", db_index=True)
    ad_type       = models.CharField(max_length=20, choices=AD_TYPES, db_index=True)
    title         = models.CharField(max_length=200)
    description   = models.TextField(blank=True)
    image_url     = models.URLField(blank=True)
    target_url    = models.URLField(blank=True)
    daily_budget  = models.DecimalField(max_digits=8, decimal_places=2, default=500)  # ৳/day
    total_budget  = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date    = models.DateField()
    end_date      = models.DateField()
    status        = models.CharField(max_length=10, choices=STATUS, default="draft", db_index=True)
    impressions   = models.PositiveBigIntegerField(default=0)
    clicks        = models.PositiveIntegerField(default=0)
    approved_by   = models.ForeignKey("accounts.User", on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name="approved_ads")
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mf_advertisements"
        ordering = ["-created_at"]
        indexes  = [
            models.Index(fields=["status", "start_date", "end_date"]),
            models.Index(fields=["hospital", "status"]),
        ]

    @property
    def ctr(self):
        """Click-through rate."""
        return round(self.clicks / self.impressions * 100, 2) if self.impressions > 0 else 0

    @property
    def remaining_budget(self):
        return round(float(self.total_budget) - float(self.amount_spent), 2)

    @property
    def is_live(self):
        today = timezone.now().date()
        return self.status == "active" and self.start_date <= today <= self.end_date

    def __str__(self):
        return f"Ad: {self.hospital} — {self.ad_type} (৳{self.total_budget})"


class AdImpression(models.Model):
    """Track every ad impression for billing."""
    ad         = models.ForeignKey(HospitalAdvertisement, on_delete=models.CASCADE,
                                   related_name="impression_logs", db_index=True)
    cost       = models.DecimalField(max_digits=6, decimal_places=4, default=0.50)  # CPM rate
    timestamp  = models.DateTimeField(auto_now_add=True, db_index=True)
    page       = models.CharField(max_length=100, blank=True)  # Which page served the ad

    class Meta:
        db_table = "mf_ad_impressions"
        indexes  = [models.Index(fields=["ad", "timestamp"])]


class Subscription(models.Model):
    PLANS = [
        ("basic",        "Basic — Free"),
        ("professional", "Professional — ৳5,000/mo"),
        ("enterprise",   "Enterprise — ৳15,000/mo"),
    ]
    FEATURES = {
        "basic":        ["Listed on directory", "Up to 5 doctors", "Basic analytics"],
        "professional": ["All Basic features", "Unlimited doctors", "Lab test booking", "Advanced analytics", "Email support"],
        "enterprise":   ["All Professional", "Priority listing", "Advertisement credits", "Custom API", "Dedicated account manager"],
    }
    hospital   = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE,
                                   related_name="subscriptions")
    plan       = models.CharField(max_length=15, choices=PLANS, default="basic")
    start_date = models.DateField()
    end_date   = models.DateField()
    amount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active  = models.BooleanField(default=True, db_index=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mf_subscriptions"
        indexes  = [models.Index(fields=["hospital", "is_active"])]

    @property
    def features(self):
        return self.FEATURES.get(self.plan, [])

    def __str__(self):
        return f"{self.hospital} — {self.plan} until {self.end_date}"


def create_commission(source_type: str, source_ref: str, hospital, gross_amount: float,
                      rate: float = 5.0) -> CommissionTransaction:
    """Helper: auto-create commission record for any booking."""
    ct = CommissionTransaction.objects.create(
        hospital=hospital,
        source_type=source_type,
        source_ref=str(source_ref),
        gross_amount=gross_amount,
        commission_rate=rate,
    )
    # Update daily snapshot
    from analytics_api.models import DailySnapshot
    snap, _ = DailySnapshot.objects.get_or_create(date=ct.created_at.date())
    snap.booking_commission = float(snap.booking_commission) + float(ct.commission_amount)
    snap.total_revenue = float(snap.total_revenue) + float(ct.commission_amount)
    snap.save(update_fields=["booking_commission", "total_revenue"])
    return ct
