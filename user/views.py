from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .models import UserDashboard, Enrollment, BankAccount, Withdraw
from .forms import ProfileUpdateForm, WithdrawalForm

# User = get_user_model()


def dashboard(request):
    # dashboard = UserDashboard.objects.prefetch_related("courses").get(user=request.user)
    # enrolled = dashboard.courses.all()
    enrolled = Enrollment.objects.select_related("course").filter(
        user_dashboard=request.user.user_dashboard
    )

    context = {"user_courses_enrollment": enrolled}
    return render(request, "user/dashboard.html", context)


def progress(request):
    in_progress = Enrollment.objects.select_related("course").filter(
        user_dashboard=request.user.user_dashboard, completed=False
    )
    context = {"user_courses_enrollment": in_progress}
    return render(request, "user/partials/user_course_list.html", context)


def completed(request):
    completed = Enrollment.objects.select_related("course").filter(
        user_dashboard=request.user.user_dashboard, completed=True
    )
    context = {"user_courses_enrollment": completed}
    return render(request, "user/partials/user_course_list.html", context)


def account_details(request):
    bank_account = BankAccount.objects.get(instructor=request.user.instructor)
    context = {"bank_account": bank_account}
    return render(request, "user/bank_account_details.html", context)


@login_required
def withdraw_funds(request):
    bank_account = BankAccount.objects.get(instructor=request.user.instructor)
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
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

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

    # if request.method == "POST":
    #     try:
    #         u_form = UserUpdateForm(request.POST, instance=request.user)
    #         p_form = ProfileUpdateForm(
    #             request.POST, request.FILES, instance=request.user.instructorprofile
    #         )
    #     except AttributeError:
    #         u_form = UserUpdateForm(request.POST, instance=request.user)
    #         p_form = ProfileUpdateForm(
    #             request.POST, request.FILES, instance=request.user.studentprofile
    #         )

    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f"Your Account has been updated!")
    #         return redirect("profile")
    # else:
    #     try:
    #         u_form = UserUpdateForm(instance=request.user)
    #         p_form = ProfileUpdateForm(instance=request.user.instructorprofile)
    #     except AttributeError:
    #         u_form = UserUpdateForm(instance=request.user)
    #         p_form = ProfileUpdateForm(instance=request.user.studentprofile)

    # context = {"u_form": u_form, "p_form": p_form}
    # return render(request, "user/profile.html", context)


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
