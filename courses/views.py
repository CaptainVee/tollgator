from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, Http404, QueryDict
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
from .models import Course, Lesson, Video, Order, Pricing
from common.utils import get_or_none
from .forms import LessonForm, VideoForm
from .utils import yt_playlist_details, yt_video_details, yt_playlist_videos


# from pypaystack import Transaction, Customer, Plan
# from paystackapi.transaction import Transaction
# from paystackapi.paystack import Paystack

User = get_user_model()


class CourseListView(ListView):
    model = Course
    template_name = "courses/home.html"
    context_object_name = "courses"
    ordering = ["-updated_at"]
    paginate_by = 5


def user_course_list_view(request):
    courses = Course.objects.select_related("author").filter(author=request.user)

    context = {"courses": courses}
    print(courses)
    return render(request, "courses/user_course_list.html", context)


class CourseDetailView(View):
    def get(self, request, course_slug, *args, **kwargs):
        course = Course.objects.select_related("pricing").get(slug=course_slug)
        order = get_or_none(Order, course=course, user=request.user)

        context = {
            "course": course,
            "order": order,
        }
        return render(request, "courses/course_detail.html", context)


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = "__all__"

    def form_valid(self, form):
        form.instance.author = get_object_or_404(User, username=self.request.user)
        form.save()
        return super().form_valid(form)


def playlist_create(request):

    if request.method == "POST":
        playlist_id = request.POST.get("playlist_id")
        yt_playlist_create_course(user=request.user, playlist_id=playlist_id)
        return redirect("courses-home")

    context = {"title": "About"}

    return render(request, "courses/playlist_form.html", context)


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ["title", "content", "image", "price"]

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
    success_url = "/"

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.author:
            return True
        return False


@login_required
def lesson_create_view(request, course_id):
    course = Course.objects.get(id=course_id)
    created_lessons = Lesson.objects.filter(course=course)
    video_form = VideoForm()
    if request.method == "POST":
        title = request.POST.get("title")
        position = request.POST.get("position")
        description = request.POST.get("description")
        lesson_form = LessonForm(request.POST)

        if lesson_form.is_valid():
            lesson = Lesson(
                title=title, course=course, position=position, description=description
            )
            lesson.save()
            # lesson_form.save()
            # context = {
            #     "lesson_form": lesson_form,
            #     "course": course,
            #     "created_lessons": created_lessons,
            # }
            # if request.htmx:
            #     return render(request, "courses/partials/resource_list.html", context)
            return redirect("lesson-detail", course_id=course_id, lesson_id=lesson.id)
    else:
        lesson_form = LessonForm()
    context = {
        "lesson_form": lesson_form,
        "course": course,
        "created_lessons": created_lessons,
        "video_form": video_form,
    }
    return render(request, "courses/lesson_form.html", context)


def lesson_list_view(request, course_slug):
    lessons = Lesson.objects.filter(course__slug=course_slug).select_related("course")

    context = {"lessons": lessons}
    return render(request, "courses/lesson_list.html", context)


def lesson_detail_view(request, lesson_id, course_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    new_url = reverse("video-create", kwargs={"lesson_id": lesson.id})
    context = {"lesson": lesson, "course_id": course_id, "new_url": new_url}
    if request.method == "GET":
        return render(request, "courses/lesson_detail.html", context)
    elif request.method == "PUT":
        data = QueryDict(request.body).dict()
        form = LessonForm(data, instance=lesson)
        if form.is_valid():
            form.save()
            return render(request, "courses/partials/lesson_update.html", context)
        context["form"] = form

        render(request, "courses/partials/lesson_update_form.html", context)


def lesson_update_view(request, lesson_id, course_id):

    lesson = get_object_or_404(Lesson, id=lesson_id)
    form = LessonForm(instance=lesson)
    context = {"lesson": lesson, "course_id": course_id, "form": form}
    return render(request, "courses/partials/lesson_update_form.html", context)


def lesson_video(request, lesson_slug, video_slug, *args, **kwargs):
    video_queryset = Video.objects.prefetch_related("lesson").filter(lesson=lesson_slug)
    video = Video.objects.get(id=video_slug)

    context = {"video_queryset": video_queryset, "video": video}
    return render(request, "courses/lesson_video.html", context)


def video_update_view(request, lesson_id=None, video_id=None):
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

        form = VideoForm(request.POST or None, instance=video)

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
            new_video.save()
            context["video"] = new_video

            return render(request, "courses/partials/video_list.html", context)

        return render(request, "courses/partials/video_form.html", context)
    else:
        raise Http404


def get_video_url(request, video_slug):
    video = Video.objects.get(id=video_slug)
    context = {"video": video}
    return render(request, "courses/partials/video_frame.html", context)


def enroll(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order = Order.objects.filter(course=course, user=request.user)
    if order:
        messages.info(request, "you have already enrolled for this course.")
    else:
        order = Order(user=request.user, course=course)
        order.save()
        messages.success(request, "You have successfully enrolled for this course.")

    return redirect("lesson-list", course_slug)


def about(request):
    return render(request, "courses/about.html", {"title": "About"})


def new(request):
    # video_list = yt_playlist_videos(playlist_id="PL1A2CSdiySGIPxpSlgzsZiWDavYTAx61d")

    # print(lister)
    return render(request, "courses/new/course-detail.html", {"title": "About"})


def clear_messages(request):
    return HttpResponse("")


@transaction.atomic
def yt_playlist_create_course(user, playlist_id):
    playlist_details = yt_playlist_details(playlist_id)
    video_list = yt_playlist_videos(playlist_id)
    try:

        course = Course.objects.create(
            author=user,
            title=playlist_details["title"],
            brief_description=playlist_details["description"],
            pricing=Pricing.objects.get(name="Free"),
        )
        try:
            lesson = Lesson.objects.create(
                course=course,
                title="Lesson 1",
                position=1,
            )
            try:
                for video in video_list:
                    Video.objects.create(
                        lesson=lesson,
                        title=video["title"],
                        position=video["position"],
                        video_url=video["video_id"],
                    )
                return redirect("courses-home")
            except:
                return HttpResponse(" Sorry o video fault")

        except:
            return HttpResponse(" Sorry o lesson fault")

    except:
        return HttpResponse(" Sorry o course fault")


def bulk_created(big_list, lesson, video):
    bulk_list = []

    for a in big_list:
        bulk_list.append(
            Video(
                lesson=lesson,
                title=video["title"],
                position=video["position"],
                video_url=video["video_id"],
            )
        )
    Video.objects.bulk_create(bulk_list, batch_size=999)


# def is_valid_form(values):
#     valid = True
#     for field in values:
#         if field == "":
#             valid = False
#     return valid


# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {"object": order}
#             return render(self.request, "courses/order_summary.html", context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("/")


# def PaymentView(request):
#     if request.user.is_authenticated:
#         # items = order.orderitem_set.all()
#         # cartItems = order.get_cart_items
#         order = Order.objects.get(user=request.user, ordered=False)
#         context = {"order": order, "pk_public": settings.PAYSTACK_PUBLIC_KEY}
#     return render(request, "courses/checkout.html", context)


# @login_required
# def add_to_cart(request, pk):
#     item = get_object_or_404(Course, pk=pk)
#     order_item, created = OrderItem.objects.get_or_create(
#         item=item, user=request.user, ordered=False
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("order-summary")
#         else:
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("order-summary")
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("order-summary")


# @login_required
# def remove_from_cart(request, pk):
#     item = get_object_or_404(Post, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item, user=request.user, ordered=False
#             )[0]
#             order.items.remove(order_item)
#             order_item.delete()
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("post-detail", pk=pk)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("post-detail", pk=pk)


# @login_required
# def remove_single_item_from_cart(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item, user=request.user, ordered=False
#             )[0]
#             if order_item.quantity > 1:
#                 order_item.quantity -= 1
#                 order_item.save()
#             else:
#                 order.items.remove(order_item)
#             messages.info(request, "This item quantity was updated.")
#             return redirect("order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("post-detail", pk=pk)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("post-detail", pk=pk)


# class VerifyView(View):
#     def get(self, request, id, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

#         # transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY )
#         # response = transaction.verify(id)
#         transaction = paystack.transaction.initialize(
#             reference=id, amount="amount", email="email"
#         )
#         response = paystack.transaction.verify(reference=id)
#         data = JsonResponse(response, safe=False)
#         # assign the payment to the order

#         order_items = order.items.all()
#         order_items.update(ordered=True)
#         for item in order_items:
#             item.save()

#         order.ordered = True
#         order.ref_code = create_ref_code()
#         order.save()

#         return render(request, "courses/verify.html", {"title": "verify"})


# class StartDetailView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         order = OrderItem.objects.filter(user=self.request.user, ordered=True)
#         if order.exists():
#             context = {"object": order}
#             return render(self.request, "courses/start.html", context)
#         else:
#             return render(self.request, "courses/start.html", {"object": None})
#         # lesson_qs = course.lessons.filter(pk=lesson_pk)
#         # if lesson_qs.exists():
#         #     lesson = lesson_qs.first()
