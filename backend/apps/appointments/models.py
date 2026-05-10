"""Appointment models"""
from django.db import models
import uuid


class Appointment(models.Model):
    STATUS = [
        ("pending","Pending"), ("confirmed","Confirmed"),
        ("completed","Completed"), ("cancelled","Cancelled"), ("no_show","No Show"),
    ]
    VISIT_TYPES = [("in_person","In Person"), ("video","Video Consult")]

    ref_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey("doctors.Doctor", on_delete=models.CASCADE, related_name="appointments")
    hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=20)
    visit_type = models.CharField(max_length=15, choices=VISIT_TYPES, default="in_person")
    status = models.CharField(max_length=15, choices=STATUS, default="pending")
    chief_complaint = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mf_appointments"
        ordering = ["-appointment_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.ref_id:
            self.ref_id = f"MF-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ref_id} | {self.patient} → Dr.{self.doctor}"
