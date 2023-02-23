from django import forms
from .models import User, Withdraw, BankAccount, Instructor
from django.db import transaction


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ["amount"]


class BankAcountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["bank_name", "account_number", "account_name"]


class BecomeInstructorForm(forms.ModelForm):
    profile_pic = forms.ImageField(label="Profile Picture", required=False)
    accept_terms_and_conditions = forms.BooleanField(
        label="I accept the terms and conditions", required=True
    )

    class Meta:
        model = Instructor
        fields = [
            "bio",
            "skills",
            "experience",
            "profile_pic",
            "accept_terms_and_conditions",
        ]
