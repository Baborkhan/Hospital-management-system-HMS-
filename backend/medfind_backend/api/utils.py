"""
Utility functions for authentication and helpers
"""

import hashlib
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hash_value):
    """Verify a password against its hash"""
    return hash_password(password) == hash_value


def create_response(data=None, message=None, status_code=status.HTTP_200_OK):
    """Create a standardized API response"""
    response_data = {
        'success': status_code < 400,
        'message': message,
        'data': data
    }
    return Response(response_data, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """Create a standardized error response"""
    return Response({
        'success': False,
        'message': message,
        'data': None
    }, status=status_code)
