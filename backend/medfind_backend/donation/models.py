from django.db import models
from api.models import Patient, Hospital

class Donation(models.Model):
    """Donation Model for blood/plasma donations"""
    donor = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='donations')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    donation_type = models.CharField(max_length=20, choices=[
        ('Blood', 'Blood'), ('Plasma', 'Plasma'), ('Platelets', 'Platelets'), ('Other', 'Other')
    ])
    blood_group = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    
    donation_date = models.DateField()
    quantity_ml = models.IntegerField()  # Quantity in ml
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')
    ])
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['donor', 'donation_date']),
            models.Index(fields=['hospital', 'donation_date']),
        ]

    def __str__(self):
        return f"{self.donation_type} donation by {self.donor}"
