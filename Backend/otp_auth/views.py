"""
MedFind — OTP API Views
Endpoints: /send-otp/ · /verify-otp/ · /resend-otp/
All return JSON with {success, message}.
"""
import json
import logging

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .services import send_otp, verify_otp, validate_email, validate_otp_code

logger = logging.getLogger(__name__)


def _parse_body(request) -> dict:
    """Safely parse JSON request body."""
    try:
        return json.loads(request.body or b'{}')
    except (json.JSONDecodeError, ValueError):
        return {}


def _json(data: dict, status: int = 200) -> JsonResponse:
    return JsonResponse(data, status=status)


# ── Point 5: Send OTP API ──────────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class SendOTPView(View):
    """
    POST /api/v1/accounts/send-otp/
    Body: {"email": "user@gmail.com"}
    Response: {success, message}

    Also handles Resend (same endpoint — services.py cancels old OTP first).
    """
    def post(self, request):
        data  = _parse_body(request)
        email = data.get('email', '').strip()

        result = send_otp(email)

        status = 200 if result['success'] else 400
        if result.get('seconds_left'):
            status = 429  # Too Many Requests
        return _json(result, status=status)

    def options(self, request, *args, **kwargs):
        response = _json({"detail": "ok"})
        response['Allow'] = 'POST, OPTIONS'
        return response


# ── Point 6: Verify OTP API ────────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTPView(View):
    """
    POST /api/v1/accounts/verify-otp/
    Body: {"email": "user@gmail.com", "otp": "123456"}
    Response: {success, message}
    """
    def post(self, request):
        data  = _parse_body(request)
        email = data.get('email', '').strip()
        code  = data.get('otp', '').strip()

        result = verify_otp(email, code)
        status = 200 if result['success'] else 400
        return _json(result, status=status)

    def options(self, request, *args, **kwargs):
        response = _json({"detail": "ok"})
        response['Allow'] = 'POST, OPTIONS'
        return response


# ── Point 9: Resend OTP API ────────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class ResendOTPView(View):
    """
    POST /api/v1/accounts/resend-otp/
    Body: {"email": "user@gmail.com"}
    Cancels old OTP, issues fresh one (handled inside send_otp service).
    Response: {success, message}
    """
    def post(self, request):
        data  = _parse_body(request)
        email = data.get('email', '').strip()

        result = send_otp(email)   # send_otp already cancels old OTPs
        status = 200 if result['success'] else 400
        if result.get('seconds_left'):
            status = 429
        return _json(result, status=status)

    def options(self, request, *args, **kwargs):
        response = _json({"detail": "ok"})
        response['Allow'] = 'POST, OPTIONS'
        return response

