from django.contrib import admin
from .models import Course, CourseRating, Lesson

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseRating)
admin.site.register(Lesson)
# admin.site.register(OrderItem)
# admin.site.register(Order)
# admin.site.register(UserProfile)
