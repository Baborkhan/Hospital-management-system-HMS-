"""Billing models"""
from django.db import models
import uuid


class Invoice(models.Model):
    TYPES = [("opd","OPD"),("pharmacy","Pharmacy"),("lab","Lab"),("admission","Admission")]
    STATUS = [("draft","Draft"),("issued","Issued"),("paid","Paid"),("cancelled","Cancelled")]
    PAYMENT = [("cash","Cash"),("bkash","bKash"),("nagad","Nagad"),("card","Card"),("bank","Bank Transfer")]

    invoice_number = models.CharField(max_length=30, unique=True, editable=False)
    hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.SET_NULL, null=True, blank=True)
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    patient_gender = models.CharField(max_length=10, blank=True)
    doctor = models.ForeignKey("doctors.Doctor", on_delete=models.SET_NULL, null=True, blank=True)
    invoice_type = models.CharField(max_length=15, choices=TYPES, default="opd")
    status = models.CharField(max_length=15, choices=STATUS, default="draft")
    payment_method = models.CharField(max_length=15, choices=PAYMENT, default="cash")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    visit_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mf_invoices"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "mf_invoice_items"
