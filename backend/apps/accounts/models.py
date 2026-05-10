"""MedFind — User & Role Management"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email: raise ValueError("Email required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra):
        extra.setdefault("role", "superadmin")
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("patient",        "Patient"),
        ("doctor",         "Doctor"),
        ("hospital_admin", "Hospital Admin"),
        ("pharmacy_admin", "Pharmacy Admin"),
        ("lab_admin",      "Lab Admin"),
        ("superadmin",     "Super Admin"),
    ]
    email        = models.EmailField(unique=True, db_index=True)
    phone        = models.CharField(max_length=20, blank=True)
    full_name    = models.CharField(max_length=200, db_index=True)
    role         = models.CharField(max_length=20, choices=ROLES, default="patient", db_index=True)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_verified  = models.BooleanField(default=False)
    avatar       = models.ImageField(upload_to="avatars/", blank=True, null=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    date_joined  = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    class Meta:
        db_table = "mf_users"
        indexes  = [
            models.Index(fields=["email"]),
            models.Index(fields=["role", "is_active"]),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    @property
    def role_display(self):
        return dict(self.ROLES).get(self.role, self.role)

    @property
    def is_platform_staff(self):
        return self.role in ("hospital_admin","pharmacy_admin","lab_admin","superadmin","doctor")
