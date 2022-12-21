from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .models import UserDashboard

# User = get_user_model()


def dashboard(request):
    enrolled = UserDashboard.objects.get(user=request.user)
    print(enrolled.courses_taken)
    context = {"user_dashboard": enrolled}
    return render(request, "user/dashboard.html", context)


@login_required
def profile(request):
    pass
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
