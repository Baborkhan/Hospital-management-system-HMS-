"""
MedFind — Doctor Fraud Detection (Spec §13)
AI-assisted check to flag potentially fake doctor accounts.
Runs automatically when a DoctorVerification is submitted.
"""
import re
import logging

logger = logging.getLogger(__name__)

# ── Risk scoring rules ────────────────────────────────────────────────────────
def _score_bmdc(bmdc: str) -> int:
    """BMDC registration number format: A-12345 or numeric 5-digit."""
    if not bmdc:
        return 30      # No BMDC number → high risk
    if re.match(r'^[A-Z]-\d{5}$', bmdc.strip().upper()):
        return 0       # Correct format
    if re.match(r'^\d{5}$', bmdc.strip()):
        return 5       # Old numeric format — acceptable
    return 20          # Malformed


def _score_name(full_name: str) -> int:
    """Flag generic/suspicious names."""
    suspicious = ["test", "doctor", "user", "admin", "fake", "demo"]
    name_lower = full_name.lower()
    for s in suspicious:
        if s in name_lower:
            return 40
    return 0


def _score_documents(verification) -> int:
    """Check if required documents are uploaded."""
    score = 0
    if not verification.license_document:
        score += 25
    if not verification.national_id:
        score += 20
    return score


def _score_qualification(qualification: str) -> int:
    """Check qualification string for known Bangladesh medical degrees."""
    valid_degrees = ["MBBS", "BDS", "MD", "MS", "FCPS", "MRCP", "MRCS", "PhD", "DPM"]
    qual_upper = qualification.upper()
    for deg in valid_degrees:
        if deg in qual_upper:
            return 0
    return 15  # No recognized degree found


# ── Main fraud check function ─────────────────────────────────────────────────
def run_fraud_check(doctor) -> dict:
    """
    Run all fraud detection rules on a Doctor + their DoctorVerification.
    Returns: {
        risk_score: 0–100,
        risk_level: "LOW" | "MEDIUM" | "HIGH",
        flags: [list of reasons],
        auto_reject: bool
    }
    """
    flags = []
    score = 0

    # BMDC number check
    bmdc_score = _score_bmdc(getattr(doctor, "bmdc_number", ""))
    if bmdc_score > 0:
        score += bmdc_score
        flags.append(f"BMDC number missing or invalid (risk +{bmdc_score})")

    # Name check
    name_score = _score_name(doctor.user.full_name)
    if name_score > 0:
        score += name_score
        flags.append(f"Suspicious account name (risk +{name_score})")

    # Qualification check
    qual_score = _score_qualification(getattr(doctor, "qualification", ""))
    if qual_score > 0:
        score += qual_score
        flags.append(f"No recognized Bangladesh medical degree found (risk +{qual_score})")

    # Document check
    try:
        ver = doctor.verification
        doc_score = _score_documents(ver)
        if doc_score > 0:
            score += doc_score
            flags.append(f"Required documents missing (risk +{doc_score})")
    except Exception:
        score += 30
        flags.append("No verification documents submitted (risk +30)")

    # Experience sanity check
    exp = getattr(doctor, "experience_years", 0)
    if exp > 60:
        score += 20
        flags.append(f"Unrealistic experience: {exp} years (risk +20)")

    # Determine risk level
    if score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    result = {
        "risk_score":  min(score, 100),
        "risk_level":  risk_level,
        "flags":       flags,
        "auto_reject": score >= 80,   # Auto-reject only extreme cases
    }

    logger.info(
        f"Fraud check for Dr.{doctor.user.full_name}: "
        f"score={result['risk_score']}, level={risk_level}"
    )
    return result
