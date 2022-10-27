import black
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_("Name of user"), blank=False, null=False, max_length=250)
    profile_pic = models.ImageField(
        blank=True, null=True, default="default.jpg", upload_to="profile_pics/"
    )
    email = models.EmailField(_("Email Address"), unique=True)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed", blank=True
    )

    def get_absolute_url(self):
        return reverse("profile")

    def __str__(self):
        return self.user.name


User = get_user_model()


class IsUser(User):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)


class InstructorProfile(models.Model):
    # user = models.OneToOneField(User, on_delete= models.CASCADE, primary_key=True)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics/')

    # def __str__(self):
    # 	return self.user.username
    pass

    @property
    def posts(self):
        return self.post_set.all().order_by("-date_posted")


class StudentProfile(models.Model):
    pass
