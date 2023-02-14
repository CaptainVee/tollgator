import random
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, Http404, QueryDict, JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from celery.result import AsyncResult
from .models import Course, Lesson, Video, WatchTime
from order.models import Order
from common.utils import get_or_none
from .forms import LessonForm, VideoForm
from .utils import (
    yt_playlist_details,
    generate_certificates,
    yt_playlist_videos,
    yt_video_duration,
    youtube_duration_convertion,
)
from .tasks import yt_playlist_create_course


# from pypaystack import Transaction, Customer, Plan
# from paystackapi.transaction import Transaction
# from paystackapi.paystack import Paystack

User = get_user_model()


class Home(View):
    """
    renders the landing page for unauthenticated users but renders
    courses list page for authenticated users
    """

    model = Course
    ordering = ["-updated_at"]
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            courses = Course.objects.filter(is_private=False)
            template = ("courses/course_list.html",)
        else:
            courses = list(Course.objects.filter(is_private=False))
            try:
                courses = random.sample(courses, 4)
            except:
                courses = Course.objects.filter(is_private=False)[:4]
            template = "courses/home.html"

        context = {
            "courses": courses,
        }
        return render(request, template, context)


class UserCourseListView(LoginRequiredMixin, ListView):
    """
    List all the courses created by an instructor
    """

    model = Course
    template_name = "courses/user_course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.select_related("author").filter(author=self.request.user)


class CourseDetailView(View):
    """
    The course detail view where user can see details about a course
    """

    def get(self, request, course_slug, *args, **kwargs):
        user = request.user
        course = Course.objects.get(slug=course_slug)
        lesson_qs = Lesson.objects.filter(course=course)
        if user.is_anonymous:
            order = None
        else:
            order = get_or_none(Order, course=course, user=request.user, ordered=True)

        context = {
            "course": course,
            "lesson_qs": lesson_qs,
            "order": order,
        }
        return render(request, "courses/course_detail.html", context)


class CourseCreateView(LoginRequiredMixin, CreateView):
    """
    For creating courses manually
    """

    model = Course
    fields = "__all__"

    def form_valid(self, form):
        form.instance.author = get_object_or_404(User, username=self.request.user)
        form.save()
        return super().form_valid(form)


@login_required
def course_create_playlist_view(request):
    """
    For creating courses from a playlist url
    """
    context = {}
    if request.method == "POST":
        # TODO ensure users does not sumbit empty forms
        playlist_id = request.POST.get("playlist_id")
        result = yt_playlist_create_course.delay(
            user_id=request.user.id, playlist_id=playlist_id
        )
        task_id = result.id
        context = {"task_id": task_id}

    return render(request, "courses/playlist_form.html", context)


# def bulk_created(big_list, lesson, video):
#     bulk_list = []

#     for a in big_list:
#         bulk_list.append(
#             Video(
#                 lesson=lesson,
#                 title=video["title"],
#                 position=video["position"],
#                 video_url=video["video_id"],
#             )
#         )
#     Video.objects.bulk_create(bulk_list, batch_size=999)


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ["title", "content", "thumbnail", "price"]

    def form_valid(self, form):
        form.instance.author = get_object_or_404(User, username=self.request.user)
        form.save()
        return super().form_valid(form)

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.author:
            return True
        return False


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = "/instructor/dashboard"
    context_object_name = "course"

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.author:
            return True
        return False


@login_required
def lesson_detail_view(request, course_id):
    """
    renders the lesson detail view page
    """

    lesson_qs = Lesson.objects.filter(course__id=course_id)

    context = {"lesson_qs": lesson_qs}

    return render(request, "courses/lesson_detail.html", context)


@login_required
def lesson_create_update(request, course_id=None, lesson_id=None):
    """
    creates and updates lessons dynamically with htmx
    """
    if request.htmx:
        try:
            course = Course.objects.get(id=course_id)
        except:
            course = None
        if course_id == None:
            return HttpResponse("NOT FOUND")

        lesson = None
        if lesson_id is not None:
            try:
                lesson = Lesson.objects.get(course=course, id=lesson_id)
            except:
                lesson = None

        form = LessonForm(request.POST or None, instance=lesson)

        form_url = reverse("lesson-new", kwargs={"course_id": course.id})
        if lesson:
            form_url = reverse(
                "lesson-detail",
                kwargs={"course_id": course.id, "lesson_id": lesson.id},
            )
        context = {
            "form_url": form_url,
            "form": form,
            "course": course,
            "lesson": lesson,
        }
        if form.is_valid():
            new_lesson = form.save(commit=False)
            if lesson is None:
                new_lesson.course = course
            new_lesson.save()
            context["lesson"] = new_lesson

            return render(request, "courses/partials/lesson_list.html", context)

        return render(request, "courses/partials/lesson_form.html", context)
    else:
        raise Http404


@login_required
def lesson_delete_view(request, course_id, lesson_id):
    try:
        lesson = Lesson.objects.select_related("course").get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404
    if request.user != lesson.course.author:
        return HttpResponse("Unauthorized Request", status=401)

    lesson.delete()

    return HttpResponse("")


@login_required
def lesson_video_view(request, course_id, video_id, *args, **kwargs):
    """
    renders the lesson video page that shows list of videos in a course
    """
    course = Course.objects.get(id=course_id)
    lesson_queryset = Lesson.objects.filter(course=course)
    last_video_watched = course.last_video_watched(user=request.user)

    try:
        start = last_video_watched.watchtime.start
    except:
        start = 0
    completed_count = Video.objects.filter(
        course=course, watchtime__finished_video=True
    ).count()
    progress = (completed_count / course.video_count) * 100

    context = {
        "lesson_queryset": lesson_queryset,
        "last_video_watched": last_video_watched,
        "course": course,
        "start": start,
        "progress": progress,
    }
    return render(request, "courses/lesson_video.html", context)


@login_required
def get_video_url(request, video_id):
    """
    gets the video url in other to pass it to the video in lesson video view
    """
    try:
        watchtime = WatchTime.objects.select_related("video").get(video__id=video_id)
        video = watchtime.video
        start = watchtime.start
    except WatchTime.DoesNotExist:
        video = Video.objects.get(id=video_id)
        start = 0

    context = {"last_video_watched": video, "start": start}

    return render(request, "courses/partials/video_frame.html", context)


@login_required
def video_create_update(request, lesson_id=None, video_id=None):
    """
    creates and updates video dynamically with htmx
    """
    if request.htmx:
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except:
            lesson = None
        if lesson_id == None:
            return HttpResponse("NOT FOUND")

        video = None
        if video_id is not None:
            try:
                video = Video.objects.get(lesson=lesson, id=video_id)
            except:
                video = None

        form = VideoForm(
            course=lesson.course, data=request.POST or None, instance=video
        )

        form_url = reverse("video-create", kwargs={"lesson_id": lesson.id})
        if video:
            form_url = reverse(
                "video-update",
                kwargs={"lesson_id": lesson.id, "video_id": video.id},
            )
        context = {
            "form_url": form_url,
            "form": form,
            "lesson": lesson,
            "video": video,
        }
        if form.is_valid():
            new_video = form.save(commit=False)
            if video is None:
                new_video.lesson = lesson
                new_video.coursev = lesson.course
            new_video.save()
            context["video"] = new_video

            return render(request, "courses/partials/video_list.html", context)

        return render(request, "courses/partials/video_form.html", context)
    else:
        raise Http404


@login_required
def video_delete_view(request, lesson_id, video_id):
    try:
        video = Video.objects.select_related("lesson").get(id=video_id)
    except Video.DoesNotExist:
        raise Http404
    if request.user != video.course.author:
        return HttpResponse("Unauthorized Request", status=401)

    video.delete()
    return HttpResponse("")


@login_required
def generate_certificate_view(request, course_id):

    return render(request, "courses/test.html", {})
    return None
    user = request.user
    course = Course.objects.get(id=course_id)
    completed_count = Video.objects.filter(
        course=course, watchtime__finished_video=True
    ).count()
    if completed_count != course.video_count:
        return HttpResponse("You haven't Completed this course yet")

    certificate = Certificate.objects.get_or_create(user=user, course=course)

    fullname = certificate.user.get_full_name

    certificate_url = generate_certificates(name=fullname, course=course.title)

    context = {"certificate_url": "http://127.0.0.1:8000/" + certificate_url}

    return render(request, "courses/certificate.html", context)


def clear_messages(request):
    """
    clears the django toast messages on click
    """
    return HttpResponse("")


def get_spinner(request):
    """
    returns spinner
    """
    return render(request, "courses/partials/spinner.html", {})


@login_required
def get_video_sidebar(request, course_id):
    """
    returns sidebar of video list
    """
    course = Course.objects.get(id=course_id)
    lesson_queryset = Lesson.objects.filter(course=course)

    context = {"lesson_queryset": lesson_queryset, "course": course}

    return render(request, "courses/partials/video_sidebar.html", context)


@csrf_exempt
def get_status(request, task_id, width):
    task_result = AsyncResult(task_id)

    if width >= 90:
        width -= 10

    context = {
        "task_id": task_id,
        "task_status": task_result.status,  # e.g 'PENDING', 'STARTED', 'SUCCESS', 'FAILURE', and 'RETRY'
        "task_result": task_result.result,  # the return value of the function
        "width": width + 10,
    }

    return render(request, "courses/partials/spinner.html", context)


@login_required
def toggle_finished_video(request, video_id):
    video = Video.objects.get(id=video_id)
    obj, _ = WatchTime.objects.get_or_create(user=request.user, video=video)
    if obj.finished_video == False:
        obj.finished_video = True
        obj.save()
        return HttpResponse(
            '<input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>'
        )
    elif obj.finished_video == True:
        obj.finished_video = False
        obj.save()
        return HttpResponse(
            '<input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">'
        )


@login_required
def watchtime_create(request):
    """-1 unstarted, 0  ended, 1  playing, 2  paused, 3  buffering, 5  video cued"""
    current_time = int(float(request.POST.get("currentTime")))
    video_id = request.POST.get("videoId")
    event = int(request.POST.get("event"))
    player_state_ended = int(request.POST.get("playerState[ENDED]"))
    player_state_playing = int(request.POST.get("playerState[PLAYING]"))
    player_state_paused = int(request.POST.get("playerState[PAUSED]"))

    try:
        video = Video.objects.get(id=video_id)
    except:
        return HttpResponse("Video not found")
    if event == player_state_paused:
        WatchTime.objects.update_or_create(
            user=request.user, video=video, defaults={"stopped_at": current_time}
        )
    elif event == player_state_ended:
        WatchTime.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={"stopped_at": current_time, "finished_video": True},
        )
    elif event == player_state_playing:
        course = Course.objects.get(id=video.get_course_id)
        course.last_video_watched = video
        course.save()
    else:
        return HttpResponse("False")

    return HttpResponse("True")


def about(request):
    return render(request, "courses/about.html", {"title": "About"})


# def lesson_detail_view(request, lesson_id, course_id, *args, **kwargs):
#     # lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson_qs = Lesson.objects.filter(course__id=course_id)
#     # new_url = reverse("video-create", kwargs={"lesson_id": lesson.id})
#     context = {"lesson_qs": lesson_qs, "course_id": course_id}
#     if request.method == "GET":
#         return render(request, "courses/lesson_detail.html", context)
#     elif request.method == "PUT":
#         data = QueryDict(request.body).dict()
#         print(data)
#         form = LessonForm(data)  # instance=lesson
#         if form.is_valid():
#             print("is valid", kwargs, args)
#             form.save()
#             print("done")
#             return render(request, "courses/partials/lesson_update.html", context)
#         context["form"] = form

#         render(request, "courses/partials/lesson_update_form.html", context)


# def lesson_list_view(request, course_slug):
#     lessons = Lesson.objects.filter(course__slug=course_slug).select_related("course")

#     context = {"lessons": lessons}
#     return render(request, "courses/lesson_list.html", context)


# @login_required
# def lesson_create_view(request, course_id):
#     course = Course.objects.get(id=course_id)
#     created_lessons = Lesson.objects.filter(course=course)
#     video_form = VideoForm()
#     if request.method == "POST":
#         title = request.POST.get("title")
#         position = request.POST.get("position")
#         description = request.POST.get("description")
#         lesson_form = LessonForm(request.POST)

#         if lesson_form.is_valid():
#             lesson = Lesson(
#                 title=title, course=course, position=position, description=description
#             )
#             lesson.save()
#             return redirect("lesson-detail", course_id=course_id, lesson_id=lesson.id)
#     else:
#         lesson_form = LessonForm()
#     context = {
#         "lesson_form": lesson_form,
#         "course": course,
#         "created_lessons": created_lessons,
#         "video_form": video_form,
#     }
#     return render(request, "courses/lesson_form.html", context)

# def lesson_update_view(request, lesson_id, course_id):

#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     form = LessonForm(instance=lesson)
#     context = {"lesson": lesson, "course_id": course_id, "form": form}
#     return render(request, "courses/partials/lesson_update_form.html", context)
