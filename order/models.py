from django.db import models
from common.models import BaseModel

from courses.models import Course
from django.conf import settings
from autoslug import AutoSlugField
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

from common.constants import ADDRESS_CHOICES, COURSE_TYPE


User = settings.AUTH_USER_MODEL


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="course_order",
    )

    def __str__(self):
        return f"{self.course} order by {self.user}"

    #     def __str__(self):


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


class Pricing(BaseModel):
    name = models.CharField(
        choices=COURSE_TYPE, max_length=50, null=False, blank=False, default="Free"
    )
    description = models.TextField()
    price = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"
