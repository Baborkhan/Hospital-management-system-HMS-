from django.db import models
from core_app.models import User

class Notification(models.Model):
    """Notification Model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=[
        ('Appointment', 'Appointment'), ('Reminder', 'Reminder'), ('Alert', 'Alert'), ('Info', 'Info')
    ])
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.user}"
