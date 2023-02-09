import black
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.db.models import Avg
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from common.models import BaseModel
from common.constants import ADDRESS_CHOICES, RATING, CATEGORY_CHOICES, COURSE_TYPE
from datetime import time


User = settings.AUTH_USER_MODEL


def get_default_currency():
    obj, created = Currency.objects.get_or_create(
        code="USD", defaults={"exchange_rate": 500}
    )
    return obj.pkid


class Course(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=150, unique=True)
    brief_description = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    slug = AutoSlugField(populate_from="title", always_update=False, unique=True)
    # tags = ArrayField(
    #     models.CharField(max_length=200, default="", blank=True),
    #     blank=True,
    #     default=list,
    # ) #Can be used only on postgress database
    thumbnail = models.ImageField(default="default.jpg", null=True, blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    total_watch_time = models.IntegerField(null=True, default=0)
    # youtube_channel = models.CharField(max_length=500, blank=True, null=True)
    # category = models.ForeignKey(
    #     "Category", on_delete=models.SET_NULL, null=True, blank=False
    # )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    currency = models.ForeignKey(
        "Currency", on_delete=models.PROTECT, default=get_default_currency
    )
    is_private = models.BooleanField(default=True)
    # last_video_watched = models.OneToOneField(
    #     "Video",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    #     related_name="last_video_watched",
    # )

    def clean(self):
        if self.price < 0:
            raise ValidationError({"price": _("price must be positive.")})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def lessons(self):
        return self.lesson_set.all().order_by("position")

    @property
    def video_count(self):
        return self.video_set.all().count()

    def last_video_watched(self, user):
        enrollment = self.enrollment_set.get(user_dashboard__user=user)
        if enrollment.last_video_watched == None:
            enrollment.last_video_watched = self.video_set.first()
        return enrollment.last_video_watched

    @property
    def get_price(self):
        course_offer = self.course_offer.filter(discounted_price__isnull=False).first()
        if course_offer:
            return course_offer.discounted_price
        else:
            return f"${self.price}"

    def get_absolute_url(self):
        return reverse("course-update", kwargs={"pk": self.pk})

    def average_rating(self):
        return self.course_rating.aggregate(Avg("value"))["value__avg"]

    def ratings(self):
        return self.course_rating.all().count()

    # def get_add_to_cart_url(self):
    #     return reverse("add-to-cart", kwargs={"pk": self.pk})

    # def get_remove_from_cart_url(self):
    #     return reverse("remove-from-cart", kwargs={"pk": self.pk})


class Lesson(BaseModel):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    position = models.IntegerField()
    description = models.CharField(max_length=250, null=True, blank=True)
    total_video_seconds = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title

    def get_course(self):
        return self.course.title

    def get_absolute_url(self):
        return reverse(
            "lesson-detail",
            kwargs={"course_slug": self.course.slug, "lesson_id": self.id},
        )

    @property
    def videos(self):
        return self.video_set.all().order_by("position")


class Video(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    video_id = models.CharField(max_length=15, null=False, blank=False)
    video_url = models.URLField(max_length=300, blank=True, null=True)
    position = models.IntegerField()
    duration_seconds = models.IntegerField(null=True, default=0)
    duration_time = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "lesson-video-detail",
            kwargs={
                "course_id": self.lesson.course.id,
                "video_id": self.id,
            },
        )


class WatchTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    finished_video = models.BooleanField(default=False)
    stopped_at = models.IntegerField(blank=True, null=True, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def start(self):
        if self.stopped_at < 10:
            return self.stopped_at
        return self.stopped_at - 5

    def __str__(self):
        return f"watch time for {self.video}"


class CourseRating(BaseModel):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="course_rating",
    )
    rated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="user_who_rated",
    )
    value = models.PositiveSmallIntegerField(
        verbose_name=_("rating value"),
        choices=RATING,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    review = models.TextField()

    def __str__(self):
        return f"{self.rated_by}"


class CourseOffer(BaseModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="course_offer",
    )
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.discounted_price < 0:
            raise ValidationError(
                {"discounted_price": _("Discounted price must be positive.")}
            )
        if self.discounted_price > self.course.price:
            raise ValidationError(
                {
                    "discounted_price": _(
                        "Discounted price cannot be higher than the regular price."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Category(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Currency(BaseModel):
    code = models.CharField(max_length=3, unique=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code
