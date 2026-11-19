from django.db import models
from django.contrib.auth.models import User


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    fee_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount_percent = models.PositiveIntegerField(default=10)
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        status = "Approved" if self.is_approved else "Pending"
        return f"{self.user.username} - {status}"