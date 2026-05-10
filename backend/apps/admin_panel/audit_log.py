"""
MedFind — Admin Audit Log
Records every important admin action: who did what and when.
Usage:
    from apps.admin_panel.audit_log import log_action
    log_action(request.user, "DOCTOR_APPROVED", f"Doctor ID {doctor.id} approved")
"""
import logging
from django.db import models
from django.conf import settings

logger = logging.getLogger("apps.admin_panel.audit")


class AdminAuditLog(models.Model):
    ACTION_CHOICES = [
        ("DOCTOR_APPROVED",    "Doctor Approved"),
        ("DOCTOR_REJECTED",    "Doctor Rejected"),
        ("HOSPITAL_ADDED",     "Hospital Added"),
        ("HOSPITAL_EDITED",    "Hospital Edited"),
        ("HOSPITAL_DELETED",   "Hospital Deleted"),
        ("USER_BANNED",        "User Banned"),
        ("USER_RESTORED",      "User Restored"),
        ("APPOINTMENT_EDITED", "Appointment Edited"),
        ("PAYMENT_REFUNDED",   "Payment Refunded"),
        ("SETTINGS_CHANGED",   "Settings Changed"),
        ("ADMIN_LOGIN",        "Admin Login"),
        ("OTHER",              "Other"),
    ]

    actor       = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.SET_NULL,
                    null=True,
                    related_name="audit_logs",
                  )
    action      = models.CharField(max_length=30, choices=ACTION_CHOICES, default="OTHER")
    description = models.TextField()
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admin Audit Log"

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.actor} → {self.action}"


def log_action(user, action: str, description: str, request=None):
    """Helper to create an audit log entry."""
    ip = None
    if request:
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR")
    try:
        AdminAuditLog.objects.create(
            actor=user,
            action=action,
            description=description,
            ip_address=ip,
        )
    except Exception as e:
        logger.warning(f"Audit log write failed: {e}")
    logger.info(f"AUDIT | {user} | {action} | {description}")
