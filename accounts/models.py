from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Account(models.Model):
    class AccountTypes(models.TextChoices):
        CHECKING = "CHECKING", "Checking"
        SAVINGS = "SAVINGS", "Savings"
        MONEY_MARKET = "MONEY_MARKET", "Money Market"
        CD = "CD", "CD"
        IRA = "IRA", "IRA"
        BROKERAGE = "BROKERAGE", "Brokerage"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        primary_key=True,
    )
    routing_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False, null=True)
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_deleted_by",
        null=True,
    )
    deleted_reason = models.TextField(null=True)
    account_type = models.CharField(
        max_length=50,
        choices=AccountTypes.choices,
        default=AccountTypes.CHECKING,
    )
