from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# User = settings.AUTH_USER_MODEL


class ProfileUpdateForm(forms.ModelForm):
    # image = forms.ImageField()

    class Meta:
        model = User
        fields = ["name", "username"]


# class StudentRegistrationForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data.get("email")
#         user.is_student = True
#         user.save()
#         student = StudentProfile.objects.create(user=user)
#         return user
