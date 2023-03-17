from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from django.http import QueryDict
from django.db.models import Prefetch
from .models import Withdraw, Instructor, BankAccount
from .forms import BankAcountForm, WithdrawalForm, BecomeInstructorForm
from courses.models import Course, CourseRating
from order.models import Order


# Create your views here.


@login_required
def become_instructor(request):
    if request.method == "POST":
        form = BecomeInstructorForm(request.POST, request.FILES)

        if form.is_valid():
            if not form.cleaned_data["accept_terms_and_conditions"]:
                form.add_error(
                    "accept_terms_and_conditions",
                    "You must accept the terms and conditions to create your profile.",
                )
                return render(
                    request, "instructor/become_instructor_form.html", {"form": form}
                )

            instructor = form.save(commit=False)
            instructor.user = request.user
            instructor.save()
            # Save the user's information in the database
            # and set the user as an instructor
            request.user.profile_pic = request.POST["profile_pic"]
            request.user.is_instructor = True
            request.user.save()
            return redirect("instructor-dashboard")
    else:
        form = BecomeInstructorForm()
    return render(request, "instructor/become_instructor_form.html", {"form": form})


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
    return render(request, "instructor/instructor_dashboard.html", context)


class OrderListView(LoginRequiredMixin, ListView):
    """
    List all the order made for an author
    """

    template_name = "instructor/order_list.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):

        orders = Order.objects.select_related("user").filter(
            course__author=self.request.user, ordered=True
        )
        return orders


@login_required
def bank_account_details(request):
    bank_account = BankAccount.objects.get(instructor=request.user.instructor)
    context = {"bank_account": bank_account}
    if request.method == "GET":
        return render(request, "user/bank_account_details.html", context)
    elif request.method == "PUT":
        data = QueryDict(request.body).dict()
        form = BankAcountForm(data, instance=bank_account)
        if form.is_valid():
            form.save()
            return render(request, "user/partials/bank_details.html", context)
        context["form"] = form
        return render(request, "user/partials/bank_account_form.html", context)


@login_required
def bank_account_edit_form(request):
    bank_account = BankAccount.objects.get(instructor=request.user.instructor)
    form = BankAcountForm(instance=bank_account)
    context = {"bank_account": bank_account, "form": form}
    return render(request, "user/partials/bank_account_form.html", context)


@login_required
def withdraw_funds(request):
    instructor = request.user.instructor
    try:
        bank_account = BankAccount.objects.get(instructor=instructor)
    except BankAccount.DoesNotExist:
        bank_account = {}
    withdrawals = Withdraw.objects.filter(instructor=instructor)

    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal_amount = int(form.cleaned_data["amount"])
            if withdrawal_amount < 50:
                messages.warning(request, "Please enter a value greater than 49 USD")
            elif withdrawal_amount > instructor.account_balance:
                messages.warning(request, "Insuficient Funds")
            else:
                instructor.account_balance -= withdrawal_amount
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
        "instructor": instructor,
        "withdrawals": withdrawals,
        "bank_account": bank_account,
        "form": form,
    }
    return render(request, "instructor/withdraw.html", context)


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
