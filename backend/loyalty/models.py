from django.db import models
class LoyaltyTransaction(models.Model):
    TYPES = [("earn","Earn"),("redeem","Redeem"),("expire","Expire"),("bonus","Bonus")]
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="loyalty_transactions")
    transaction_type = models.CharField(max_length=10, choices=TYPES)
    points = models.IntegerField()
    description = models.CharField(max_length=300)
    balance_after = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "mf_loyalty_transactions"
        ordering = ["-created_at"]
