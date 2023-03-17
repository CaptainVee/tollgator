from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel, Currency

# from common.utils import get_default_currency

from courses.models import Course, Video


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
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)

    def get_absolute_url(self):
        return reverse("profile")

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        if self.name:
            return self.name
        return self.username

    @property
    def courses(self):
        return self.course_set.all().order_by("created_at")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


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


class Enrollment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_dashboard = models.ForeignKey(UserDashboard, on_delete=models.CASCADE)
    last_video_watched = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="last_video_watched",
    )
    completed = models.BooleanField(default=False)
    completed_on = models.DateField(blank=True, null=True)
