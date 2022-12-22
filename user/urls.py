from django.urls import path


from .views import profile, dashboard, progress, completed


urlpatterns = [
    path("profile/", profile, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/in-progress", progress, name="in-progress"),
    path("dashboard/completed", completed, name="completed"),
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
