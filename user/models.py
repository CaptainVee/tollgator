import black
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

from courses.models import Course, Lesson


class User(AbstractUser):
    name = models.CharField(_("Name of user"), blank=False, null=False, max_length=250)
    first_name = None
    last_name = None
    email = models.EmailField(_("Email Address"), unique=True)
    username = models.CharField(
        verbose_name=_("username"), db_index=True, max_length=255, unique=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_instructor = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("profile")

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return self.name

    @property
    def posts(self):
        return self.courses_set.all().order_by("-date_posted")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


User = get_user_model()


class UserDashboard(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_dashboard"
    )
    courses = models.ManyToManyField(
        Course, related_name="courses", blank=True, through="Enrollment"
    )

    def __str__(self):
        return self.user.username

    @property
    def get_full_name(self):
        return self.user.name

    class Meta:
        verbose_name = _("user dashboard")
        verbose_name_plural = _("user dashboards")


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Instructor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Enrollment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(UserDashboard, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_on = models.DateField(blank=True, null=True)
