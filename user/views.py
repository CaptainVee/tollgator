from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    UserUpdateForm,
    ProfileUpdateForm,
    InstuctorRegistrationForm,
    StudentRegistrationForm,
)
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.models import User


class InstructorRegisterView(CreateView):
    model = User
    form_class = InstuctorRegistrationForm
    template_name = "user/register.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "instructor"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("login")


class StudentRegisterView(CreateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = "user/register.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("login")


@login_required
def profile(request):
    if request.method == "POST":
        try:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.instructorprofile
            )
        except AttributeError:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.studentprofile
            )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your Account has been updated!")
            return redirect("profile")
    else:
        try:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.instructorprofile)
        except AttributeError:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.studentprofile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "user/profile.html", context)
