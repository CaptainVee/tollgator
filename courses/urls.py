from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostDetailView,
    LessonCreateView,
    LessonListView,
    lesson_video,
    get_video_url,
    LessonDetailView,
)  # , VerifyView, Enroll

# from .views import  add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView, , StartDetailView


urlpatterns = [
    path("", PostListView.as_view(), name="courses-home"),
    path("user/<int:pk>/", UserPostDetailView.as_view(), name="user-post"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path(
        "post/<int:pk>/<slug:course_slug>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
    path(
        "<slug:course_slug>/lesson/<int:lesson_slug>/",
        LessonListView.as_view(),
        name="lesson-list",
    ),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    # path("about/", views.about, name="courses-about"),
    # path('enroll/<int:pk>/', Enroll, name='enroll'),
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
        "video/<slug:video_slug>",
        get_video_url,
        name="video-url",
    ),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    # path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    # path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    # path('remove-item-from-cart/<int:pk>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
    # path('payment/', PaymentView, name='payment'),
    # path('verify/<int:id>/', VerifyView.as_view(), name='verify'),
    # path('start/', StartDetailView.as_view(), name='start'),
]
