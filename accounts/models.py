from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta


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


class CardTypes(models.TextChoices):
    CREDIT = "CREDIT", "Credit"
    DEBIT = "DEBIT", "Debit"
    REWARDS = "REWARDS", "Rewards"


class CardProviders(models.TextChoices):
    VISA = "VISA", "Visa"
    MASTERCARD = "MASTERCARD", "Mastercard"
    AMEX = "AMEX", "American Express"


def generate_card_number():
    return random.randint(10**15, 10**16 - 1)


def generate_cvv():
    return random.randint(100, 999)


class Card(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    card_number = models.BigIntegerField(
        unique=True,
        primary_key=True,
        editable=False,
        default=generate_card_number,
    )
    cvv = models.IntegerField(
        default=generate_cvv,
    )
    expiration_date = models.DateField(default=datetime.now() + relativedelta(years=+4))
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
        related_name="card_deleted_by",
        null=True,
    )
    deleted_reason = models.TextField(null=True)
    card_type = models.CharField(
        max_length=50,
        choices=CardTypes.choices,
        default=CardTypes.DEBIT,
    )
    card_provider = models.CharField(
        max_length=50,
        choices=CardProviders.choices,
        default=CardProviders.VISA,
    )


class CreditCard(Card):
    card_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_due_date = models.DateField()
    minimum_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.card_type = CardTypes.CREDIT
        super().save(*args, **kwargs)


class DebitCard(Card):
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    weekly_limit = models.DecimalField(max_digits=10, decimal_places=2, default=2500.00)
    monthly_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=8000.00
    )
    transaction_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=10000.00
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="debit_cards",
        null=True,
    )

    def save(self, *args, **kwargs):
        self.card_type = CardTypes.DEBIT
        super().save(*args, **kwargs)


class RewardsCard(CreditCard):
    rewards = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rewards_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rewards_available = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    rewards_used = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rewards_expiration = models.DateField()

    def save(self, *args, **kwargs):
        self.card_type = CardTypes.REWARDS
        super().save(*args, **kwargs)


@receiver(post_save, sender=Account)
def create_debit_card(sender, instance, created, **kwargs):
    if created:
        DebitCard.objects.create(
            account=instance,
            user=instance.user,
        )
