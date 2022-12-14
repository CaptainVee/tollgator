from email.policy import default
import black
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from common.models import BaseModel
from common.constants import ADDRESS_CHOICES, RATING, CATEGORY_CHOICES, COURSE_TYPE
from courses.utils import yt_video_duration, youtube_duration_convertion
from datetime import time


User = settings.AUTH_USER_MODEL


class Course(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    brief_description = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField()
    slug = AutoSlugField(populate_from="title", always_update=False, unique=True)
    # tags = ArrayField(
    #     models.CharField(max_length=200, default="", blank=True),
    #     blank=True,
    #     default=list,
    # ) #Can be used only on postgress database
    thumbnail = models.ImageField(default="default.jpg", null=True, blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    duration = models.IntegerField(null=True, default=0)
    # youtube_channel = models.CharField(max_length=500, blank=True, null=True)
    # category = models.ForeignKey(
    #     "Category", on_delete=models.SET_NULL, null=True, blank=False
    # )
    pricing = models.ForeignKey(
        "Pricing", on_delete=models.SET_NULL, null=True, blank=False
    )

    def __str__(self):
        return self.title

    def get_pricing(self):
        return self.pricing.price

    @property
    def lessons(self):
        return self.lesson_set.all().order_by("position")

    def get_absolute_url(self):
        return reverse("course-update", kwargs={"pk": self.pk})

    # def get_add_to_cart_url(self):
    #     return reverse("add-to-cart", kwargs={"pk": self.pk})

    # def get_remove_from_cart_url(self):
    #     return reverse("remove-from-cart", kwargs={"pk": self.pk})


class Lesson(BaseModel):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    position = models.IntegerField()
    description = models.CharField(max_length=250, null=True, blank=True)
    total_video_length = models.FloatField(null=True, blank=True)

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

    @property
    def videos_duration(self):
        i = 0
        for a in self.video_set.all():
            i += a.duration_seconds
        return i


class Video(BaseModel):
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

    @property
    def videos(self):
        return self.video_set.all().order_by("position")

    @property
    def video_seconds(self):
        # self.video_duration = 0
        # self.save()
        if self.duration_seconds <= 0:
            duration = yt_video_duration(self.video_id)
            video_seconds, total_time = youtube_duration_convertion(duration)
            self.duration_seconds = int(video_seconds)
            self.duration_time = total_time
            self.save()
        return f"{self.duration_time}"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="course_order",
    )

    def __str__(self):
        return f"{self.course} order by {self.user}"


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
    value = models.IntegerField(
        verbose_name=_("rating value"),
        choices=RATING,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    review = models.TextField()

    def __str__(self):
        return self.course


class Pricing(BaseModel):
    name = models.CharField(
        choices=COURSE_TYPE, max_length=50, null=False, blank=False, default="Free"
    )
    description = models.TextField()
    price = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"


# class OrderItem(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     item = models.ForeignKey(Course, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.item.title}"

#     def get_total_item_price(self):
#         return self.quantity * self.item.price

#     def get_total_discount_item_price(self):
#         return self.quantity * self.item.discount_price

#     def get_amount_saved(self):
#         return self.get_total_item_price() - self.get_total_discount_item_price()

#     def get_final_price(self):
#         if self.item.discount_price:
#             return self.get_total_discount_item_price()
#         return self.get_total_item_price()
