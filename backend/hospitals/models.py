"""Hospital models"""
from django.db import models


class Division(models.TextChoices):
    DHAKA = "Dhaka", "Dhaka"
    CHITTAGONG = "Chittagong", "Chittagong"
    RAJSHAHI = "Rajshahi", "Rajshahi"
    SYLHET = "Sylhet", "Sylhet"
    KHULNA = "Khulna", "Khulna"
    BARISAL = "Barisal", "Barisal"
    RANGPUR = "Rangpur", "Rangpur"
    MYMENSINGH = "Mymensingh", "Mymensingh"


class Hospital(models.Model):
    TYPE_CHOICES = [("government", "Government"), ("private", "Private"), ("clinic", "Clinic")]

    name = models.CharField(max_length=300, db_index=True)
    hospital_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="private")
    division = models.CharField(max_length=20, choices=Division.choices)
    district = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    total_beds = models.PositiveIntegerField(default=0)
    available_beds = models.PositiveIntegerField(default=0)
    icu_total = models.PositiveIntegerField(default=0)
    icu_available = models.PositiveIntegerField(default=0)
    emergency_open = models.BooleanField(default=False)
    has_icu = models.BooleanField(default=False)
    has_pharmacy = models.BooleanField(default=False)
    has_lab = models.BooleanField(default=False)
    specialties = models.JSONField(default=list, blank=True)
    services = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mf_hospitals"
        ordering = ["-rating", "name"]

    def __str__(self):
        return self.name

    @property
    def bed_occupancy_rate(self):
        if self.total_beds == 0:
            return 0
        return round((self.total_beds - self.available_beds) / self.total_beds * 100, 1)


class HospitalAdmin(models.Model):
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name="admin_profile")
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mf_hospital_admins"

    def __str__(self):
        return f"Admin: {self.user.full_name} → {self.hospital.name}"


class HospitalService(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital_services")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "mf_hospital_services"

    def __str__(self):
        return f"{self.hospital.name} - {self.name}"


class HospitalBankAccount(models.Model):
    """
    Spec §6 — Hospital Bank Integration
    Payment settlement details for each hospital.
    """
    SETTLEMENT_CHOICES = [
        ("daily",   "Daily Payout"),
        ("weekly",  "Weekly Payout"),
        ("monthly", "Monthly Payout"),
    ]

    hospital            = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name="bank_account")
    # Bank transfer
    bank_name           = models.CharField(max_length=100, blank=True)
    account_name        = models.CharField(max_length=200, blank=True)
    account_number      = models.CharField(max_length=50, blank=True)
    routing_number      = models.CharField(max_length=20, blank=True)
    branch_name         = models.CharField(max_length=100, blank=True)
    # Mobile banking
    bkash_number        = models.CharField(max_length=15, blank=True)
    nagad_number        = models.CharField(max_length=15, blank=True)
    rocket_number       = models.CharField(max_length=15, blank=True)
    # Settlement preference
    settlement_preference = models.CharField(max_length=10, choices=SETTLEMENT_CHOICES, default="weekly")
    preferred_method    = models.CharField(
        max_length=15,
        choices=[("bank", "Bank Transfer"), ("bkash", "bKash"), ("nagad", "Nagad"), ("rocket", "Rocket")],
        default="bank"
    )
    is_verified         = models.BooleanField(default=False)   # Admin verifies bank details
    verified_by         = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"role": "superadmin"}, related_name="verified_bank_accounts"
    )
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mf_hospital_bank_accounts"

    def __str__(self):
        return f"{self.hospital.name} — {self.preferred_method} ({self.settlement_preference})"
