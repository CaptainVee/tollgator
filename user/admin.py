from django.contrib import admin
from .models import UserDashboard
from django.contrib.auth import get_user_model

User = get_user_model()


admin.site.register(UserDashboard)
admin.site.register(User)

# Register your models here.
