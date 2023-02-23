from django.db import models
from common.models import BaseModel

# from courses.models import Course
from django.conf import settings
from autoslug import AutoSlugField
from django_countries import fields, Countries
from django.utils.translation import gettext_lazy as _

from common.constants import (
    ADDRESS_CHOICES,
    COURSE_TYPE,
    PAYMENT_METHODS,
    PAYMENT_PROVIDER,
    TRANSACTION_STATUSES,
)

# class G8Countries(Countries):
#     only = [
#         'CA', 'FR', 'DE', 'IT', 'JP', 'RU', 'GB',
#         ('EU', _('European Union'))
#     ]

User = settings.AUTH_USER_MODEL


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="course_order",
    )
    ordered = models.BooleanField(default=False)


#         return f"{self.quantity} of {self.item.title}"

#     def get_total_item_price(self):
#         return self.quantity * self.item.price

#     def get_total_discount_item_price(self):
#         return self.quantity * self.item.discount_price

#     def get_amount_saved(self):
#         return self.get_total_item_price() - self.get_total_discount_item_price()

#     def get_final_price(self):
#         if self.item.discount_price:
#             return self.get_total_discount_item_price()
#         return self.get_total_item_price()


class Cart(BaseModel):
    reference = models.CharField(max_length=100, null=False, blank=False)
    orders = models.ManyToManyField(Order)
    total_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    # country = fields.CountryField()

    @property
    def get_first_course(self):
        print("tjjkjrjtkrjtkrjtktr", self.orders)
        return self.orders.first().course


class Transaction(BaseModel):
    transaction_ref = models.CharField(max_length=100, null=False, blank=False)
    cart = models.OneToOneField(Cart, null=False, blank=False, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHODS, null=False, blank=False
    )
    payment_provider = models.CharField(
        max_length=50, choices=PAYMENT_PROVIDER, null=False, blank=False
    )
    discount = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    vat = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    total_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    verified = models.BooleanField(default=False)
    transaction_status = models.CharField(
        max_length=200,
        choices=TRANSACTION_STATUSES,
        null=True,
        blank=True,
        default="Pending Payment",
    )
    transaction_description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.cart.user.get_full_name + " - " + self.transaction_ref


# class Pricing(BaseModel):
#     name = models.CharField(
#         choices=COURSE_TYPE, max_length=50, null=False, blank=False, default="Free"
#     )
#     description = models.TextField()
#     price = models.FloatField(default=0, null=False, blank=False)

#     def __str__(self):
#         return self.name
