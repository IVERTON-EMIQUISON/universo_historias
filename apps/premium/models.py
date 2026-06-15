from django.db import models

# Create your models here.
from django.db import models
from apps.accounts.models import User


class PremiumPlan(models.Model):
    name = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    stripe_price_id_monthly = models.CharField(max_length=100, blank=True)
    stripe_price_id_yearly = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)


class Subscription(models.Model):
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    
    PERIOD_CHOICES = [
        (MONTHLY, 'Mensal'),
        (YEARLY, 'Anual'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(PremiumPlan, on_delete=models.CASCADE)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)