from django.db import models
class Notification(models.Model):
    TYPES = [("appointment","Appointment"),("order","Order"),("system","System"),("alert","Alert"),("video","Video Call")]
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "mf_notifications"
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.user} - {self.title}"
