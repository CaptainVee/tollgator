from django.contrib import admin
from .models import InstructorProfile, StudentProfile , IsUser


admin.site.register(InstructorProfile)
admin.site.register(StudentProfile)
admin.site.register(IsUser)

# Register your models here.
