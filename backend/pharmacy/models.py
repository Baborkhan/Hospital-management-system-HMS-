"""Pharmacy models"""
from django.db import models
import uuid


class Medicine(models.Model):
    TYPES = [("otc","OTC"),("rx","Prescription"),("generic","Generic")]
    CATEGORIES = [
        ("pain","Pain Relief"),("antibiotic","Antibiotic"),("vitamin","Vitamin"),
        ("diabetes","Diabetes"),("cardiac","Cardiac"),("skin","Skin"),
        ("eye","Eye"),("child","Pediatric"),("supplement","Supplement"),
        ("allergy","Allergy"),("gastro","Gastro"),("respiratory","Respiratory"),
    ]
    name = models.CharField(max_length=200, db_index=True)
    generic_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    medicine_type = models.CharField(max_length=10, choices=TYPES, default="otc")
    category = models.CharField(max_length=20, choices=CATEGORIES, default="pain")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50, default="strip/10")
    stock_quantity = models.PositiveIntegerField(default=100)
    description = models.TextField(blank=True)
    dosage = models.CharField(max_length=200, blank=True)
    side_effects = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mf_medicines"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.generic_name})"

    @property
    def stock_status(self):
        if self.stock_quantity == 0: return "out"
        if self.stock_quantity < 20: return "low"
        return "in"


class PharmacyOrder(models.Model):
    STATUS = [
        ("pending","Pending"),("confirmed","Confirmed"),("packed","Packed"),
        ("dispatched","Dispatched"),("delivered","Delivered"),("cancelled","Cancelled"),
    ]
    PAYMENT = [("cash","Cash"),("bkash","bKash"),("nagad","Nagad"),("card","Card"),("bank","Bank")]

    ref_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="pharmacy_orders", null=True, blank=True)
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS, default="pending")
    payment_method = models.CharField(max_length=10, choices=PAYMENT, default="cash")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=50)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    has_prescription = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mf_pharmacy_orders"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.ref_id:
            self.ref_id = f"MF-PH-{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ref_id} | {self.patient_name}"


class PharmacyOrderItem(models.Model):
    order = models.ForeignKey(PharmacyOrder, on_delete=models.CASCADE, related_name="items")
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "mf_pharmacy_order_items"

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
