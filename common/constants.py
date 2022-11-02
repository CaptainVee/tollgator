from django.utils.translation import gettext_lazy as _

YES_NO_EMPTY_OPTION = (
    ("", "-----"),
    ("Yes", "Yes"),
    ("No", "No"),
)
CATEGORY_CHOICES = (
    ("IT and Software", "IT and Software"),
    ("Law", "Law"),
    ("Entertainment", "Entertainment"),
)

PAYMENT_METHODS = (("payment_card", "Payment Card"), ("bank_transfer", "Bank Transfer"))

ADDRESS_CHOICES = (
    ("B", "Billing"),
    ("S", "Shipping"),
)
RATING = (
    (1, _("poor")),
    (2, _("fair")),
    (3, _("good")),
    (4, _("very good")),
    (5, _("excellent")),
)

COURSE_TYPE = (
    ("Free", "Free"),
    ("Certificate", "Certificate"),
    ("Paid", "Paid"),
)
