from django.contrib import admin

from .models import Instructor, BankAccount, Withdraw

# Register your models here.

admin.site.register(BankAccount)
admin.site.register(Instructor)
admin.site.register(Withdraw)
