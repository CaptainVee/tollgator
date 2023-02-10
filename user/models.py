import black
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

from courses.models import Course, Video
from common.constants import PAYOUT_STATUS


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
        return self.email

    @property
    def get_full_name(self):
        return self.name

    @property
    def courses(self):
        return self.course_set.all().order_by("created_at")

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


class Instructor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class BankAccount(BaseModel):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=False, blank=False
    )
    country = models.CharField(max_length=50, blank=False, null=False)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=False, null=False)
    account_name = models.CharField(max_length=50, blank=False, null=False)
    account_balance = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.bank_name}-{self.account_number}"


class Withdraw(BaseModel):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.PositiveIntegerField(null=False, blank=False)
    # comment = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(choices=PAYOUT_STATUS, max_length=20, default="Initiated")

    def __str__(self) -> str:
        return f"{self.instructor}-{self.amount}"

    # define a save methos or use signal to ensure no withdrwal is made when a user has less than that in hi account


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
