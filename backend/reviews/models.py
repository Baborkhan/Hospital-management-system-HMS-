"""Reviews & Ratings"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    TYPES = [("doctor","Doctor"),("hospital","Hospital")]

    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="reviews")
    review_type = models.CharField(max_length=10, choices=TYPES)
    doctor = models.ForeignKey("doctors.Doctor", on_delete=models.CASCADE, null=True, blank=True, related_name="reviews")
    hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE, null=True, blank=True, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mf_reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review {self.rating}★ by {self.patient}"
