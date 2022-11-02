from django.contrib import admin
from .models import Course, CourseRating, Lesson, Video, Order, Pricing, Category

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseRating)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Order)
admin.site.register(Pricing)
admin.site.register(Category)
# admin.site.register(Pricing)
