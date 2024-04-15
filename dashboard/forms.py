from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date, timedelta


inputs_classes = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-color-3-500 focus:border-color-3-500 block w-full p-2.5 "


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        widget=forms.TextInput(attrs={"class": inputs_classes}),
        error_messages={
            "required": "This field is required",
            "invalid": "Enter a valid email address",
        },
    )

    username = forms.CharField(
        max_length=30,
        help_text="Required. Inform a valid username.",
        widget=forms.TextInput(attrs={"class": inputs_classes}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": inputs_classes}),
        label="Password",
        help_text=(
            "Your password can't be too similar to your other personal information.<br>"
            "Your password must contain at least 8 characters.<br>"
            "Your password can't be a commonly used password.<br>"
            "Your password can't be entirely numeric."
        ),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": inputs_classes}),
        label="Repeat your password",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        help_text="Required. Inform a valid username.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": inputs_classes,
            }
        ),
        label="Password",
    )


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        help_text="Required. Inform your first name.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    last_name = forms.CharField(
        max_length=100,
        help_text="Required. Inform your last name.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    phone = forms.CharField(
        max_length=10,
        help_text="Required. Inform your phone number.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    address = forms.CharField(
        help_text="Required. Inform your address.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    city = forms.CharField(
        max_length=50,
        help_text="Required. Inform your city.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    state = forms.CharField(
        max_length=50,
        help_text="Required. Inform your state.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    zip = forms.CharField(
        max_length=6,
        help_text="Required. Inform your zip code.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    country = forms.CharField(
        max_length=50,
        help_text="Required. Inform your country.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "class": inputs_classes,
                "type": "date",
                "min": "1900-01-01",
                "max": date.today() - timedelta(days=18 * 365),
            },
            format="%Y-%m-%d",
        ),
    )

    ssn = forms.CharField(
        max_length=9,
        help_text="Required. Inform your social security number.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    annual_income = forms.IntegerField(
        help_text="Required. Inform your annual income.",
        widget=forms.NumberInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    occupation = forms.CharField(
        max_length=50,
        help_text="Required. Inform your occupation.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )


class EmploymentForm(forms.Form):
    is_employed = forms.BooleanField(
        label="Are you employed?",
        widget=forms.CheckboxInput(
            attrs={
                "class": "text-gray-900",
            }
        ),
    )

    employer = forms.CharField(
        max_length=50,
        help_text="Your company or employer name.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    employer_address = forms.CharField(
        help_text="Employer address.",
        widget=forms.TextInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )


class InvestmentForm(forms.Form):
    is_investor = forms.BooleanField(
        label="Are you an investor?",
        widget=forms.CheckboxInput(
            attrs={
                "class": "text-gray-900",
            }
        ),
    )

    investment_amount = forms.IntegerField(
        label="Estimated yearly investment amount",
        widget=forms.NumberInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    investment_duration = forms.IntegerField(
        label="Estimated investment duration in months",
        widget=forms.NumberInput(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    investment_risk = forms.ChoiceField(
        label="Whats the maximum risk you are willing to take?",
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        widget=forms.Select(
            attrs={
                "class": inputs_classes,
            }
        ),
    )

    investment_type = forms.ChoiceField(
        help_text="What type of investment are you looking for? (stocks, bonds, funds, etc.)",
        choices=[
            ("stocks", "Stocks"),
            ("bonds", "Bonds"),
            ("funds", "Funds"),
            ("other", "Other"),
        ],
        widget=forms.Select(
            attrs={
                "class": inputs_classes,
            },
        ),
    )

    investment_return = forms.IntegerField(
        label="Expected return in percentage.",
        widget=forms.NumberInput(
            attrs={
                "class": inputs_classes,
                "min": 0,
                "max": 100,
            },
        ),
    )

    investment_purpose = forms.ChoiceField(
        label="What's your investment purpose?",
        choices=[
            ("retirement", "Retirement"),
            ("education", "Education"),
            ("wealth", "Wealth"),
            ("savings", "Savings"),
            ("other", "Other"),
        ],
        widget=forms.Select(
            attrs={
                "class": inputs_classes,
            },
        ),
    )
