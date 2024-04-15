from django.db import models
from django.contrib.auth.models import User
from enum import Enum

# Create your models here.


class OnboardingStep(Enum):
    PERSONAL_INFO = "PERSONAL_INFO"
    EMPLOYMENT_INFO = "EMPLOYMENT_INFO"
    INVESTMENT_INFO = "INVESTMENT_INFO"
    COMPLETE = "COMPLETE"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", unique=True, null=True
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, default="", null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=6, null=True)
    country = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=True)
    ssn = models.CharField(max_length=9, null=True)
    annual_income = models.IntegerField(null=True)
    occupation = models.CharField(max_length=50, null=True)
    is_employed = models.BooleanField(null=True)
    employer = models.CharField(max_length=50, null=True)
    employer_address = models.TextField(null=True)
    is_investor = models.BooleanField(null=True)
    investment_amount = models.IntegerField(null=True)
    investment_duration = models.IntegerField(null=True)
    investment_risk = models.CharField(max_length=50, null=True)
    investment_type = models.CharField(max_length=50, default="none", null=True)
    investment_return = models.IntegerField(default=0, null=True)
    investment_purpose = models.CharField(max_length=50, null=True)
    is_insured = models.BooleanField(default=False, null=True)
    insurance_type = models.CharField(max_length=50, default="none", null=True)
    insurance_coverage = models.IntegerField(default=0, null=True)
    insurance_duration = models.IntegerField(default=0, null=True)
    onboarding_step = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in OnboardingStep],
        default=OnboardingStep.PERSONAL_INFO,
        null=True,
    )
