"""Doctor models"""
from django.db import models


class Doctor(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="doctor_profile")
    hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")
    bmdc_number = models.CharField(max_length=50, unique=True, blank=True)
    specialty = models.CharField(max_length=100)
    sub_specialty = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=500)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500)
    video_fee = models.DecimalField(max_digits=8, decimal_places=2, default=400)
    bio = models.TextField(blank=True)
    available_days = models.JSONField(default=list)
    available_hours = models.CharField(max_length=100, blank=True, default="9:00 AM - 5:00 PM")
    languages = models.JSONField(default=list)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    total_patients = models.PositiveIntegerField(default=0)
    is_available_today = models.BooleanField(default=True)
    accepts_video_consult = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mf_doctors"
        ordering = ["-rating", "specialty"]

    def __str__(self):
        return f"Dr. {self.user.full_name} ({self.specialty})"


class DoctorSchedule(models.Model):
    DAYS = [
        ("Saturday", "Saturday"), ("Sunday", "Sunday"), ("Monday", "Monday"),
        ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"), ("Friday", "Friday"),
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="schedules")
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_slots = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "mf_doctor_schedules"
        unique_together = ["doctor", "day"]


class DoctorVerification(models.Model):
    """
    Spec §4 — Doctor Verification System
    Tracks uploaded documents and approval status (PENDING → VERIFIED / REJECTED)
    """
    STATUS = [
        ("PENDING",  "Pending Review"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
    ]

    doctor              = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name="verification")
    # Required documents (spec §4)
    license_document    = models.FileField(upload_to="verifications/licenses/", null=True, blank=True)
    national_id         = models.FileField(upload_to="verifications/nid/",      null=True, blank=True)
    hospital_affiliation= models.FileField(upload_to="verifications/affiliation/", null=True, blank=True)
    live_photo          = models.ImageField(upload_to="verifications/photos/",  null=True, blank=True)

    status              = models.CharField(max_length=10, choices=STATUS, default="PENDING", db_index=True)
    rejection_reason    = models.TextField(blank=True)  # Admin fills on REJECTED
    reviewed_by         = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"role": "superadmin"}, related_name="verifications_reviewed"
    )
    submitted_at        = models.DateTimeField(auto_now_add=True)
    reviewed_at         = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "mf_doctor_verifications"

    def __str__(self):
        return f"Verification({self.doctor} — {self.status})"

    def approve(self, admin_user):
        from django.utils import timezone
        self.status      = "VERIFIED"
        self.reviewed_by = admin_user
        self.reviewed_at = timezone.now()
        self.save()
        # Sync to Doctor profile
        self.doctor.is_verified = True
        self.doctor.save(update_fields=["is_verified"])

    def reject(self, admin_user, reason=""):
        from django.utils import timezone
        self.status           = "REJECTED"
        self.rejection_reason = reason
        self.reviewed_by      = admin_user
        self.reviewed_at      = timezone.now()
        self.save()
        self.doctor.is_verified = False
        self.doctor.save(update_fields=["is_verified"])
