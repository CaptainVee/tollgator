from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from order.models import Order
from .models import UserDashboard, Enrollment
from .forms import ProfileUpdateForm


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
def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, f"Your Account has been updated!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        "form": form,
    }
    return render(request, "user/profile.html", context)
