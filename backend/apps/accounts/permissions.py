"""
MedFind — Role-Based Permission System
Roles: patient | doctor | hospital_admin | pharmacy_admin | lab_admin | superadmin
"""
from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """Only superadmin (platform owner)."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == "superadmin")


class IsHospitalAdmin(BasePermission):
    """Hospital admin — manages one hospital."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ("hospital_admin", "superadmin"))


class IsPharmacyAdmin(BasePermission):
    """Pharmacy admin — manages medicine stock."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ("pharmacy_admin", "hospital_admin", "superadmin"))


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ("doctor", "superadmin"))


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ("patient", "superadmin"))


class IsLabAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ("lab_admin", "hospital_admin", "superadmin"))


class IsStaff(BasePermission):
    """Any staff member (not patient)."""
    STAFF_ROLES = ("doctor", "hospital_admin", "pharmacy_admin", "lab_admin", "superadmin")
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in self.STAFF_ROLES)


class IsAuthenticatedReadOnly(BasePermission):
    """Read = any authenticated user. Write = staff only."""
    STAFF_ROLES = ("doctor", "hospital_admin", "pharmacy_admin", "lab_admin", "superadmin")
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user.role in self.STAFF_ROLES
