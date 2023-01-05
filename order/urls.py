from django.urls import path
from .views import enroll, checkout, verify


urlpatterns = [
    path(
        "course/<slug:course_id>/enroll/",
        enroll,
        name="enroll",
    ),
    path(
        "checkout/<slug:cart_id>/",
        checkout,
        name="checkout",
    ),
    path(
        "verify/transaction/<slug:transaction_id>/",
        verify,
        name="verify-transaction",
    ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
