# auctions/models.py
from django.db import models
from django.contrib.auth.models import User

class Operation(models.Model):
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_required = models.DecimalField(max_digits=10, decimal_places=2)
    annual_interest = models.DecimalField(max_digits=5, decimal_places=2)
    deadline = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Operation by {self.operator} for {self.amount_required}"

class Bid(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, related_name="bids", on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.investor} for {self.bid_amount} at {self.interest_rate}%"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)  

    def __str__(self):
        return self.user.username
