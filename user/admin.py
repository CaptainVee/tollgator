from django.contrib import admin
from .models import Dashboard, UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


admin.site.register(UserProfile)
admin.site.register(Dashboard)
admin.site.register(User)

# Register your models here.
