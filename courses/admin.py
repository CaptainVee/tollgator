from django.contrib import admin
from .models import Course, CourseRating, Lesson, LessonVideo

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseRating)
admin.site.register(Lesson)
admin.site.register(LessonVideo)
# admin.site.register(Order)
# admin.site.register(UserProfile)
