import black
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from courses.models import Course


class User(AbstractUser):
    name = models.CharField(_("Name of user"), blank=False, null=False, max_length=250)
    first_name = None
    last_name = None
    email = models.EmailField(_("Email Address"), unique=True)
    username = models.CharField(
        verbose_name=_("username"), db_index=True, max_length=255, unique=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("profile")

    def __str__(self):
        return self.username

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile"
    )
    profile_pic = models.ImageField(
        blank=True, null=True, default="default.jpg", upload_to="profile_pics/"
    )
    cover_image = models.ImageField(
        default="default.jpg", upload_to="profile_pics/", blank=True, null=True
    )

    followers_count = models.IntegerField(blank=True, null=True, default=0)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed", blank=True
    )

    def __str__(self):
        return self.user.username

    def get_name(self):
        return self.user.name

    @property
    def posts(self):
        return self.post_set.all().order_by("-date_posted")

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")


class Dashboard(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_dashboard"
    )
    courses_taken = models.ManyToManyField(Course, related_name="courses_taken")
    courses_completed = models.ManyToManyField(Course, related_name="courses_completed")

    def __str__(self):
        return self.user.username


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def posts(self):
        return self.post_set.all().order_by("-date_posted")
