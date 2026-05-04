from django.db import models
class Campaign(models.Model):
    TYPES = [("banner","Banner Ad"),("featured","Featured Listing"),("awareness","Awareness Campaign")]
    hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE, related_name="campaigns")
    campaign_type = models.CharField(max_length=15, choices=TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "mf_campaigns"
