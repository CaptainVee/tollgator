from django.urls import path
from .views import enroll


urlpatterns = [
    path(
        "course/<slug:course_slug>/enroll/",
        enroll,
        name="enroll",
    ),
]


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
