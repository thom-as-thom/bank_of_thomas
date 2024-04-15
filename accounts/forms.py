from django import forms
from .models import Account

inputs_classes = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-color-3-500 focus:border-color-3-500 block w-full p-2.5 "


class CreateBankAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["account_type"]
        widgets = {
            "account_type": forms.Select(attrs={"class": inputs_classes}),
        }
