from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from courses.models import Lesson, Video, CourseRating

from django.forms import ModelChoiceField


PAYMENT_CHOICES = (("S", "Stripe"), ("P", "PayPal"))


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ["is_deleted", "course", "total_video_length"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["lesson", "title", "video_url", "position"]

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["lesson"].queryset = Lesson.objects.filter(course=course)


class CourseRatingForm(forms.ModelForm):
    class Meta:
        model = CourseRating
        fields = ["value", "review"]
