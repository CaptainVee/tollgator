from django.urls import path


from .views import profile, dashboard


urlpatterns = [
    path("profile/", profile, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
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
