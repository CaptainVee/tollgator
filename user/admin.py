from django.contrib import admin
from .models import UserDashboard, Enrollment, Instructor, BankAccount, Withdraw
from django.contrib.auth import get_user_model

User = get_user_model()


admin.site.register(UserDashboard)
admin.site.register(Enrollment)
admin.site.register(BankAccount)
admin.site.register(Instructor)
admin.site.register(Withdraw)
admin.site.register(User)

# Register your models here.
