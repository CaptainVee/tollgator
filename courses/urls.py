from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    LessonCreateView,
    lesson_list_view,
    lesson_video,
    get_video_url,
    LessonDetailView,
    enroll,
)

# from .views import  add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView, , StartDetailView


urlpatterns = [
    path("", PostListView.as_view(), name="courses-home"),
    path("course/new/", PostCreateView.as_view(), name="course-create"),
    path(
        "course/<slug:course_slug>/",
        PostDetailView.as_view(),
        name="course-detail",
    ),
    path("course/<int:pk>/update", PostUpdateView.as_view(), name="course-update"),
    path("course/<int:pk>/delete", PostDeleteView.as_view(), name="course-delete"),
    # path("about/", views.about, name="courses-about"),
    path(
        "course/<slug:course_slug>/lessons",
        lesson_list_view,
        name="lesson-list",
    ),
    path(
        "lesson/<int:course_pk>/new/", LessonCreateView.as_view(), name="lesson-create"
    ),
    path(
        "<slug:course_slug>/lesson/<slug:lesson_slug>/",
        LessonDetailView.as_view(),
        name="lesson-detail",
    ),
    path(
        "<slug:course_slug>/lesson/<slug:lesson_slug>/<slug:video_slug>",
        lesson_video,
        name="lesson-video-detail",
    ),
    path(
        "course/<slug:course_slug>/enroll",
        enroll,
        name="enroll",
    ),
]


htmx_urlpatterns = [
    path(
        "video/<slug:video_slug>",
        get_video_url,
        name="video-url",
    ),
]

urlpatterns += htmx_urlpatterns
