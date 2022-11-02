from django.contrib import admin
from .models import Dashboard, UserProfile


admin.site.register(UserProfile)
admin.site.register(Dashboard)

# Register your models here.
