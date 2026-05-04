from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User Model"""
    role = models.CharField(max_length=20, choices=[
        ('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin'), ('Staff', 'Staff')
    ], default='Patient')
    
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.URLField(blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='core_app_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='core_app_user_set',
        related_query_name='user',
    )
    
    def __str__(self):
        return self.username
