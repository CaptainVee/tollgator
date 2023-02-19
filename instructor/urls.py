from django.urls import path
from .views import (
    bank_account_details,
    withdraw_funds,
    instructor_dashboard,
    bank_account_edit_form,
    OrderListView,
)


urlpatterns = [
    path("dashboard/", instructor_dashboard, name="instructor-dashboard"),
    path(
        "dashboard/bank-account-details/",
        bank_account_details,
        name="bank-account-details",
    ),
    path("dashboard/withdraw-funds/", withdraw_funds, name="withdraw-funds"),
    path(
        "dashboard/orders",
        OrderListView.as_view(),
        name="order-list",
    ),
    path(
        "dashboard/bank-account-form/",
        bank_account_edit_form,
        name="bank-account-edit-form",
    )
    # path(
    #     "register/instructor",
    #     InstructorRegisterView.as_view(),
    #     name="instructor-register",
    # ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns