from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserDashboard

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **Kwargs):
    if created:
        UserDashboard.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **Kwargs):
#     instance.save()
