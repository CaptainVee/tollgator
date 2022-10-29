from django.contrib import admin
from .models import InstructorProfile, StudentProfile, User, UserProfile


admin.site.register(User)
admin.site.register(UserProfile)
# admin.site.register(IsUser)

# Register your models here.
