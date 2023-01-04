from django.urls import path
from .views import enroll, checkout, verify


urlpatterns = [
    path(
        "course/<slug:course_id>/enroll/",
        enroll,
        name="enroll",
    ),
    path(
        "checkout/<slug:id>/",
        checkout,
        name="checkout",
    ),
    path(
        "verify/transaction/",
        verify,
        name="verify-transaction",
    ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
