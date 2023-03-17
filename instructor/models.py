from django.db import models
from django.conf import settings

from common.models import BaseModel
from common.constants import PAYOUT_STATUS


# Create your models here.
User = settings.AUTH_USER_MODEL


class Instructor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    accept_terms_and_conditions = models.BooleanField(default=False)
    account_balance = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.user.username


class BankAccount(BaseModel):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=False, blank=False
    )
    country = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.bank_name}-{self.account_number}"


class Withdraw(BaseModel):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.PositiveIntegerField(null=False, blank=False)
    # comment = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(choices=PAYOUT_STATUS, max_length=20, default="Initiated")

    def __str__(self) -> str:
        return f"{self.instructor}-{self.amount}"

    # TODO define a save methos or use signal to ensure no withdrwal is made when a user has
    # less than that in hi account
