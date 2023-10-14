from django.contrib.auth.models import User
from django.db import models



class PrivateKey(models.Model):
    key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.key

class NFT(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    movie_created_for = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    wallet_address = models.CharField(max_length=100, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    private_key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of ${self.amount:.2f} by {self.user.username}"
