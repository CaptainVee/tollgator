from django.db import models
from django.contrib.auth.models import User, AbstractUser


class IsUser(User):
	is_student = models.BooleanField(default=False)
	is_instructor = models.BooleanField(default=False)

class InstructorProfile(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE, primary_key=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return self.user.username 

	@property
	def posts(self):
		return self.post_set.all().order_by('-date_posted')

class StudentProfile(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE, primary_key=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{ self.user.username } Profile'

# Create your models here.
