"""Lab Tests"""
from django.db import models
import uuid


class LabTest(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.CharField(max_length=100)
    hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE, related_name="lab_tests", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sample_type = models.CharField(max_length=100, blank=True)
    turnaround_hours = models.PositiveIntegerField(default=24)
    is_home_collection = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "mf_lab_tests"

    def __str__(self):
        return f"{self.name} - ৳{self.price}"


class LabBooking(models.Model):
    STATUS = [("pending","Pending"),("sample_collected","Sample Collected"),("processing","Processing"),("completed","Completed"),("cancelled","Cancelled")]

    ref_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20)
    test = models.ForeignKey(LabTest, on_delete=models.PROTECT)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    is_home_collection = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    result_file = models.FileField(upload_to="lab_results/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mf_lab_bookings"

    def save(self, *args, **kwargs):
        if not self.ref_id:
            self.ref_id = f"MF-LAB-{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
