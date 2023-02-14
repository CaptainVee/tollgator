from django.urls import path


from .views import (
    profile,
    dashboard,
    progress,
    completed,
    account_details,
    withdraw_funds,
    instructor_dashboard,
    OrderListView,
)


urlpatterns = [
    path("profile/", profile, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard2/", instructor_dashboard, name="dashboard2"),
    path("dashboard/in-progress/", progress, name="in-progress"),
    path("dashboard/completed/", completed, name="completed"),
    path("dashboard/account-details/", account_details, name="account-details"),
    path("dashboard/withdraw-funds/", withdraw_funds, name="withdraw-funds"),
    path(
        "dashboard/orders",
        OrderListView.as_view(),
        name="order-list",
    ),
    # path(
    #     "register/instructor",
    #     InstructorRegisterView.as_view(),
    #     name="instructor-register",
    # ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
