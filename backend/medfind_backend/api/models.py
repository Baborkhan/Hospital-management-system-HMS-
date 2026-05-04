"""
Models for MEDFIND - Hospital Management System
Using Django ORM with SQLite
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import json


class Hospital(models.Model):
    """Hospital Model"""
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    address = models.JSONField()  # Store address as JSON
    logo = models.URLField(blank=True)
    website = models.URLField(blank=True)
    license_number = models.CharField(max_length=100, unique=True)
    
    # Features and facilities
    specialties = models.JSONField(default=list)  # List of specialties
    bed_count = models.IntegerField(null=True)
    ambulance_available = models.BooleanField(default=True)
    emergency_services = models.BooleanField(default=True)
    
    # Rating and reviews
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    
    # Operating hours
    working_hours = models.JSONField(default=list)  # List of working hours
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Doctor Model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    qualifications = models.JSONField(default=list)
    experience_years = models.IntegerField(null=True)
    
    # Hospital association
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    # Availability and schedule
    consultation_fee = models.FloatField()
    available_days = models.JSONField(default=list)  # List of days
    working_hours = models.JSONField(null=True)  # Working hours as JSON
    
    # Rating
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    
    # Additional info
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True)
    license_number = models.CharField(max_length=100, unique=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['specialization']),
            models.Index(fields=['hospital', 'specialization']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Patient(models.Model):
    """Patient Model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=255, blank=True)
    
    # Personal info
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    
    # Contact details
    address = models.JSONField(null=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Medical history
    medical_conditions = models.JSONField(default=list)
    allergies = models.JSONField(default=list)
    medications = models.JSONField(default=list)
    
    # Account info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    """Appointment Model"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=20, choices=[
        ('In-Person', 'In-Person'), ('Online', 'Online'), ('Phone', 'Phone')
    ])
    
    reason_for_visit = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('No-Show', 'No-Show')
    ])
    
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor}"


class LabTest(models.Model):
    """Laboratory Test Model"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    test_name = models.CharField(max_length=100)
    test_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)  # e.g., 'Blood', 'X-Ray', 'Ultrasound'
    cost = models.FloatField()
    
    test_date = models.DateField(null=True)
    result_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')
    ])
    
    result = models.JSONField(null=True)  # Store test results as JSON
    report_file = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['patient', 'test_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.test_name} - {self.patient}"


class Billing(models.Model):
    """Billing/Invoice Model"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    
    # Line items
    services = models.JSONField(default=list)  # List of services with cost
    total_amount = models.FloatField()
    discount = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    payable_amount = models.FloatField()
    
    # Payment info
    payment_method = models.CharField(max_length=20, choices=[
        ('Cash', 'Cash'), ('Card', 'Card'), ('Cheque', 'Cheque'), ('Online Transfer', 'Online Transfer')
    ], blank=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed'), ('Refunded', 'Refunded')
    ])
    paid_date = models.DateField(null=True)
    
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['patient', 'invoice_date']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Invoice: {self.invoice_number}"


class Pharmacy(models.Model):
    """Medicine/Pharmacy Model"""
    medicine_name = models.CharField(max_length=100, unique=True)
    medicine_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    # Medical details
    generic_name = models.CharField(max_length=100, blank=True)
    strength = models.CharField(max_length=50, blank=True)  # e.g., '500mg'
    form = models.CharField(max_length=20, choices=[
        ('Tablet', 'Tablet'), ('Capsule', 'Capsule'), ('Liquid', 'Liquid'),
        ('Injection', 'Injection'), ('Cream', 'Cream'), ('Other', 'Other')
    ])
    
    # Inventory
    quantity_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(null=True)
    price = models.FloatField()
    
    # Supplier info
    supplier_name = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(null=True)
    
    # Hospital association
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['medicine_name']),
            models.Index(fields=['medicine_code']),
            models.Index(fields=['hospital', 'medicine_name']),
        ]

    def __str__(self):
        return self.medicine_name


class MedicalHistory(models.Model):
    """Medical History Record Model"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    record_date = models.DateField(auto_now_add=True)
    visit_type = models.CharField(max_length=50, blank=True)  # e.g., 'Check-up', 'Follow-up', 'Emergency'
    
    symptoms = models.JSONField(default=list)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Vital signs
    vital_signs = models.JSONField(null=True)  # e.g., {'blood_pressure': '120/80', 'temperature': '98.6'}
    
    # Follow-up
    follow_up_date = models.DateField(null=True)
    follow_up_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['patient', 'record_date']),
            models.Index(fields=['hospital', 'record_date']),
        ]

    def __str__(self):
        return f"Medical Record: {self.patient} - {self.record_date}"
