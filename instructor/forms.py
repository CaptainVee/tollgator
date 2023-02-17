from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Withdraw, BankAccount
from django.db import transaction


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ["amount"]


class BankAcountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["bank_name", "account_number", "account_name"]


class InstuctorRegistrationForm(UserCreationForm):
    pass
    # email = forms.EmailField()

    # class Meta:
    #     model = User
    #     fields = ["username", "email", "password1", "password2"]

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data.get("email")
    #     user.is_student = True
    #     user.save()
    #     student =objects.create(user=user)
    #     return user
