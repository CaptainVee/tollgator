from django.urls import path


from .views import (
    profile,
    dashboard,
    progress,
    completed,
    account_details,
    withdraw_funds,
)


urlpatterns = [
    path("profile/", profile, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/in-progress/", progress, name="in-progress"),
    path("dashboard/completed/", completed, name="completed"),
    path("dashboard/account-details/", account_details, name="account-details"),
    path("dashboard/withdraw-funds/", withdraw_funds, name="withdraw-funds"),
    # path(
    #     "register/student",
    #     StudentRegisterView.as_view(),
    #     name="student-register",
    # ),
    # path(
    #     "register/instructor",
    #     InstructorRegisterView.as_view(),
    #     name="instructor-register",
    # ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
