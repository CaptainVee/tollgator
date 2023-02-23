from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Instructor, BankAccount


@receiver(post_save, sender=Instructor)
def create_bank_account(sender, instance, created, **kwargs):
    if created:
        BankAccount.objects.create(instructor=instance)
