from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import InstructorProfile, StudentProfile

@receiver(post_save, sender=InstructorProfile)
def create_profile(sender, instance, created, **Kwargs):
	if created:
		InstructorProfile.objects.create(user=instance)

@receiver(post_save, sender=StudentProfile)
def create_profile(sender, instance, created, **Kwargs):
	if created:
		StudentProfile.objects.create(user=instance)


@receiver(post_save, sender=InstructorProfile)
def save_profile(sender, instance, **Kwargs):
	instance.instructorprofile.save()

@receiver(post_save, sender=StudentProfile)
def save_profile(sender, instance, **Kwargs):
	instance.studentprofile.save()


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **Kwargs):
# 	if created:
# 		form = UserRegistrationForm()
# 		# if kwargs['types'] == 'instructor':
# 		username = form.cleaned_data.get('username')
# 		InstructorProfile.objects.create(user=instance)
# 	else:
# 		StudentProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **Kwargs):
# 	instance.instructorprofile.save()