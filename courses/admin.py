from django.contrib import admin
from .models import (
    Course,
    CourseRating,
    CourseOffer,
    Lesson,
    Video,
    WatchTime,
    Category,
    Currency,
)

# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(CourseRating)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(WatchTime)
admin.site.register(Category)
admin.site.register(CourseOffer)
admin.site.register(Currency)
# admin.site.register(Pricing)
