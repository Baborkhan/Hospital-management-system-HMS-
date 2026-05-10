"""
MedFind — EmailOTP Model
Handles OTP generation, storage, expiry, and rate limiting.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta


class EmailOTP(models.Model):
    """
    Stores a single active OTP per email.
    - created_at  : when the OTP was generated
    - expires_at  : exactly 2 minutes after created_at
    - is_used     : True once verified (immediately invalidated)
    - attempt_count: tracks failed verify attempts (brute-force guard)
    """
    email        = models.EmailField(db_index=True)
    otp          = models.CharField(max_length=6)
    created_at   = models.DateTimeField(auto_now_add=True)
    expires_at   = models.DateTimeField()
    is_used      = models.BooleanField(default=False)
    attempt_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table  = 'mf_email_otp'
        ordering  = ['-created_at']
        indexes   = [models.Index(fields=['email', 'is_used'])]

    def save(self, *args, **kwargs):
        # Set expiry to exactly 2 minutes from creation (point 7)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired

    def __str__(self):
        return f"OTP({self.email}) expires={self.expires_at} used={self.is_used}"

