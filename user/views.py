from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from order.models import Order
from courses.models import Course, CourseRating, CourseOffer
from .models import UserDashboard, Enrollment, BankAccount, Withdraw
from .forms import ProfileUpdateForm, WithdrawalForm


@login_required
def dashboard(request):
    # dashboard = UserDashboard.objects.prefetch_related("courses").get(user=request.user)
    # enrolled = dashboard.courses.all()
    enrolled = Enrollment.objects.select_related("course").filter(
        user_dashboard=request.user.user_dashboard
    )

    context = {"user_courses_enrollment": enrolled}
    return render(request, "user/dashboard.html", context)


@login_required
def instructor_dashboard(request):

    courses = (
        Course.objects.filter(author=request.user)
        .select_related("author")
        .prefetch_related(
            Prefetch("course_rating", queryset=CourseRating.objects.all()),
        )
    )
    total_enrollment = 0
    total_revenue = 0
    course_ratings = []
    # courses = request.user.courses.order_by("-created_at")
    for course in courses:
        total_revenue += course.get_total_revenue()
        course_ratings.append(course.get_average_rating())
        total_enrollment += course.get_enrollment_count()
    page = request.GET.get("page", 1)  # get current page number from request parameters
    paginator = Paginator(courses, 5)  # create a Paginator object with 5 items per page
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        courses = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        courses = paginator.page(paginator.num_pages)

    # Calculate the average rating for all the courses authored by the author
    if len(course_ratings) > 0:
        avg_rating = round(sum(course_ratings) / len(course_ratings), 1)
    else:
        avg_rating = None

    context = {
        "courses": courses,
        "total_revenue": total_revenue,
        "avg_rating": avg_rating,
        "total_enrollment": total_enrollment,
    }
    return render(request, "courses/user_course_list.html", context)


@login_required
def progress(request):
    in_progress = Enrollment.objects.select_related("course").filter(
        user_dashboard=request.user.user_dashboard, completed=False
    )
    context = {"user_courses_enrollment": in_progress}
    return render(request, "user/partials/user_course_list.html", context)


@login_required
def completed(request):
    completed = Enrollment.objects.select_related("course").filter(
        user_dashboard=request.user.user_dashboard, completed=True
    )
    context = {"user_courses_enrollment": completed}
    return render(request, "user/partials/user_course_list.html", context)


@login_required
def account_details(request):
    bank_account = BankAccount.objects.get(instructor=request.user.instructor)
    context = {"bank_account": bank_account}
    return render(request, "user/bank_account_details.html", context)


class OrderListView(LoginRequiredMixin, ListView):
    """
    List all the order made for an author
    """

    template_name = "user/user_order_list.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.select_related("user").filter(
            course__author=self.request.user, ordered=True
        )


@login_required
def withdraw_funds(request):
    try:
        bank_account = BankAccount.objects.get(instructor=request.user.instructor)
    except BankAccount.DoesNotExist:
        bank_account = {}
    withdrawals = Withdraw.objects.filter(instructor=request.user.instructor)

    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal_amount = int(form.cleaned_data["amount"])
            if withdrawal_amount < 5000:
                messages.warning(request, "Please enter a value greater than 5000")
            elif withdrawal_amount > bank_account.account_balance:
                messages.warning(request, "Insuficient Funds")
            else:
                bank_account.account_balance -= withdrawal_amount
                bank_account.save()
                withdrawal = form.save(commit=False)
                withdrawal.instructor = request.user.instructor
                withdrawal.save()
                messages.success(
                    request,
                    "Your request has been initiated, please note it may take up to 24hrs for the transaction to be fufilled.",
                )
            return redirect("withdraw-funds")
    else:
        form = WithdrawalForm()
    context = {
        "bank_account": bank_account,
        "withdrawals": withdrawals,
        "form": form,
    }
    return render(request, "user/withdraw.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f"Your Accounthas been updated!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        "form": form,
    }
    return render(request, "user/profile.html", context)


# class InstructorRegisterView(CreateView):
#     model = User
#     form_class = InstuctorRegistrationForm
#     template_name = "user/register.html"

#     def get_context_data(self, **kwargs):
#         kwargs["user_type"] = "instructor"
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return redirect("login")
