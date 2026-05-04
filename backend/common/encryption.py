"""
MedFind — Medical Data Encryption Utility
Uses Fernet symmetric encryption for sensitive medical fields.

Setup:
    pip install cryptography

    In .env:
    FIELD_ENCRYPTION_KEY=<generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">

Usage:
    from apps.common.encryption import encrypt_field, decrypt_field

    # Encrypting before save:
    patient.diagnosis_notes = encrypt_field(raw_notes)

    # Decrypting after read:
    raw_notes = decrypt_field(patient.diagnosis_notes)
"""
import os
import base64
import logging

logger = logging.getLogger(__name__)

_fernet = None

def _get_fernet():
    global _fernet
    if _fernet is None:
        try:
            from cryptography.fernet import Fernet
            key = os.getenv("FIELD_ENCRYPTION_KEY", "")
            if not key:
                logger.warning(
                    "FIELD_ENCRYPTION_KEY not set. Medical field encryption disabled. "
                    "Set this env var in production!"
                )
                return None
            _fernet = Fernet(key.encode())
        except ImportError:
            logger.warning("cryptography package not installed. Run: pip install cryptography")
    return _fernet


def encrypt_field(plain_text: str) -> str:
    """Encrypt a string field. Returns encrypted string or original if encryption unavailable."""
    if not plain_text:
        return plain_text
    f = _get_fernet()
    if f is None:
        return plain_text  # Graceful degradation
    try:
        return f.encrypt(plain_text.encode()).decode()
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        return plain_text


def decrypt_field(encrypted_text: str) -> str:
    """Decrypt an encrypted field. Returns decrypted string or original if decryption unavailable."""
    if not encrypted_text:
        return encrypted_text
    f = _get_fernet()
    if f is None:
        return encrypted_text
    try:
        return f.decrypt(encrypted_text.encode()).decode()
    except Exception:
        # Not encrypted (legacy plain text field)
        return encrypted_text
