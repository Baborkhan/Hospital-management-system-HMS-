"""
MedFind — OTP Service Layer
All OTP business logic lives here (generate, send, verify, rate-limit).
"""
import random
import re
import logging
from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import EmailOTP

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────
OTP_EXPIRY_MINUTES  = 2          # Point 7: exact 2-minute expiry
RATE_LIMIT_SECONDS  = 60         # Point 10: 1 OTP per 60 seconds
MAX_VERIFY_ATTEMPTS = 5          # brute-force guard per OTP
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')


# ── Point 4: OTP Generator ──────────────────────────────────────────────────
def generate_otp() -> str:
    """Return a cryptographically-safe 6-digit OTP string (zero-padded)."""
    return str(random.SystemRandom().randint(100_000, 999_999))


# ── Point 1 (Input Validation) helper ──────────────────────────────────────
def validate_email(email: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)."""
    if not email or not isinstance(email, str):
        return False, "Email address is required."
    email = email.strip().lower()
    if not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email address."
    if len(email) > 254:
        return False, "Email address is too long."
    return True, ""


def validate_otp_code(code: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message). Point 11."""
    if not code or not isinstance(code, str):
        return False, "OTP code is required."
    code = code.strip()
    if not re.fullmatch(r'\d{6}', code):
        return False, "OTP must be exactly 6 digits."
    return True, ""


# ── Point 10: Rate Limiter ──────────────────────────────────────────────────
def check_rate_limit(email: str) -> tuple[bool, int]:
    """
    Checks if email is rate-limited.
    Returns (is_limited, seconds_remaining).
    Allowed: 1 OTP per RATE_LIMIT_SECONDS window.
    """
    cutoff = timezone.now() - timedelta(seconds=RATE_LIMIT_SECONDS)
    recent = (
        EmailOTP.objects
        .filter(email=email.lower(), created_at__gte=cutoff)
        .order_by('-created_at')
        .first()
    )
    if recent:
        elapsed  = (timezone.now() - recent.created_at).total_seconds()
        remaining = max(0, int(RATE_LIMIT_SECONDS - elapsed))
        return True, remaining
    return False, 0


# ── Point 5: Send OTP (generate + save + email) ────────────────────────────
def send_otp(email: str) -> dict:
    """
    Full send flow:
      1. Validate email format
      2. Rate-limit check
      3. Cancel old OTPs (resend / point 9)
      4. Generate + save new OTP
      5. Send email via Gmail SMTP
    Returns dict: {success, message, ?seconds_left}
    """
    # Step 1 — validate
    ok, err = validate_email(email)
    if not ok:
        return {"success": False, "message": err}

    email = email.strip().lower()

    # Step 2 — rate limit
    limited, seconds_left = check_rate_limit(email)
    if limited:
        return {
            "success": False,
            "message": f"Please wait {seconds_left} seconds before requesting a new OTP.",
            "seconds_left": seconds_left,
        }

    # Step 3 — invalidate all existing OTPs for this email (point 9)
    EmailOTP.objects.filter(email=email, is_used=False).update(is_used=True)

    # Step 4 — generate & persist
    code = generate_otp()
    otp_obj = EmailOTP.objects.create(email=email, otp=code)

    # Step 5 — send email
    try:
        _send_otp_email(email, code, otp_obj.expires_at)
        logger.info("OTP sent to %s (id=%d)", email, otp_obj.pk)
        return {
            "success": True,
            "message": "OTP sent to your email. It expires in 2 minutes.",
        }
    except Exception as exc:
        # If email fails, mark the OTP as used so user can retry
        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])
        logger.error("Failed to send OTP to %s: %s", email, exc)
        return {
            "success": False,
            "message": "Failed to send OTP email. Please check your email address and try again.",
        }


def _send_otp_email(email: str, code: str, expires_at):
    """Build and dispatch the OTP email via Gmail SMTP."""
    from_email  = settings.EMAIL_HOST_USER
    expires_str = expires_at.strftime("%I:%M %p")  # e.g. 03:45 PM

    subject = "🔐 Your MedFind Login Code"
    text_body = (
        f"Your MedFind OTP is: {code}\n\n"
        f"This code expires at {expires_str} (2 minutes).\n"
        f"Do NOT share this code with anyone.\n\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"— MedFind Bangladesh Team"
    )
    html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MedFind OTP</title></head>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:40px 0;">
    <tr><td align="center">
      <table width="520" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.10);">

        <!-- Header -->
        <tr><td style="background:linear-gradient(135deg,#1a56db,#0d9488);padding:32px 40px;text-align:center;">
          <h1 style="margin:0;color:#ffffff;font-size:24px;font-weight:800;letter-spacing:-.5px;">
            🏥 MedFind Bangladesh
          </h1>
          <p style="margin:6px 0 0;color:rgba(255,255,255,.75);font-size:13px;">Secure Login Verification</p>
        </td></tr>

        <!-- Body -->
        <tr><td style="padding:36px 40px;">
          <p style="margin:0 0 8px;color:#374151;font-size:15px;font-weight:600;">Hello,</p>
          <p style="margin:0 0 24px;color:#6b7280;font-size:14px;line-height:1.6;">
            Use the code below to complete your MedFind login.
            This code is valid for <strong>2 minutes only</strong>.
          </p>

          <!-- OTP Box -->
          <div style="background:#f0fdf4;border:2px dashed #0d9488;border-radius:12px;padding:28px;text-align:center;margin-bottom:24px;">
            <p style="margin:0 0 8px;color:#0d9488;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">
              Your One-Time Password
            </p>
            <span style="font-size:42px;font-weight:900;letter-spacing:12px;color:#1a56db;font-family:'Courier New',monospace;">
              {code}
            </span>
            <p style="margin:12px 0 0;color:#6b7280;font-size:12px;">
              ⏰ Expires at {expires_str} — do not share this code
            </p>
          </div>

          <div style="background:#fff7ed;border-left:4px solid #f59e0b;border-radius:6px;padding:12px 16px;margin-bottom:16px;">
            <p style="margin:0;color:#92400e;font-size:12px;line-height:1.5;">
              ⚠️ <strong>Security Notice:</strong> MedFind will never ask for your OTP via phone or chat.
              If you did not request this, please ignore this email.
            </p>
          </div>
        </td></tr>

        <!-- Footer -->
        <tr><td style="background:#f9fafb;padding:20px 40px;text-align:center;border-top:1px solid #e5e7eb;">
          <p style="margin:0;color:#9ca3af;font-size:12px;">
            © 2026 MedFind Bangladesh · Automated message, do not reply.
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""
    send_mail(
        subject=subject,
        message=text_body,
        from_email=f"MedFind Bangladesh <{from_email}>",
        recipient_list=[email],
        html_message=html_body,
        fail_silently=False,
    )


# ── Point 6: Verify OTP (match + expiry check) ─────────────────────────────
def verify_otp(email: str, code: str) -> dict:
    """
    Verification flow:
      1. Validate inputs
      2. Find the latest active OTP for this email
      3. Check expiry
      4. Check code match
      5. Immediately delete/invalidate on success (point 8)
    Returns dict: {success, message}
    """
    # Step 1 — validate inputs (point 11)
    ok, err = validate_email(email)
    if not ok:
        return {"success": False, "message": err}

    ok2, err2 = validate_otp_code(code)
    if not ok2:
        return {"success": False, "message": err2}

    email = email.strip().lower()
    code  = code.strip()

    # Step 2 — find the latest unused OTP
    otp_obj = (
        EmailOTP.objects
        .filter(email=email, is_used=False)
        .order_by('-created_at')
        .first()
    )

    if not otp_obj:
        return {"success": False, "message": "No OTP found for this email. Please request a new one."}

    # Step 3 — check expiry (point 7)
    if otp_obj.is_expired:
        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])
        return {"success": False, "message": "OTP has expired. Please request a new one."}

    # Brute-force guard
    otp_obj.attempt_count += 1
    if otp_obj.attempt_count >= MAX_VERIFY_ATTEMPTS:
        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used", "attempt_count"])
        return {
            "success": False,
            "message": "Too many failed attempts. Please request a new OTP.",
        }
    otp_obj.save(update_fields=["attempt_count"])

    # Step 4 — match
    if otp_obj.otp != code:
        attempts_left = MAX_VERIFY_ATTEMPTS - otp_obj.attempt_count
        return {
            "success": False,
            "message": f"Incorrect OTP. {attempts_left} attempt(s) remaining.",
        }

    # Step 5 — success: immediately invalidate (point 8)
    otp_obj.is_used = True
    otp_obj.save(update_fields=["is_used"])

    logger.info("OTP verified for %s (id=%d)", email, otp_obj.pk)
    return {"success": True, "message": "OTP verified successfully."}

