from django import forms
from django.utils.translation import gettext_lazy as _
from courses.models import Course, Lesson, Video, CourseRating


PAYMENT_CHOICES = (("S", "Stripe"), ("P", "PayPal"))


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "price",
            "brief_description",
            "thumbnail",
            "content",
            "is_private",
        ]
        labels = {
            "title": _("Course Title"),
            "content": _("Course Content"),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ["is_deleted", "course", "total_video_seconds"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["lesson", "title", "video_id", "position"]

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["lesson"].queryset = Lesson.objects.filter(course=course)


class CourseRatingForm(forms.ModelForm):
    class Meta:
        model = CourseRating
        fields = ["value", "review"]
