from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import InstructorProfile, StudentProfile
from django.db import transaction

class InstuctorRegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.email = self.cleaned_data.get('email')
		user.is_student = True
		user.save()
		student = InstructorProfile.objects.create(user=user)
		return user


class StudentRegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.email = self.cleaned_data.get('email')
		user.is_student = True
		user.save()
		student = StudentProfile.objects.create(user=user)
		return user

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	image = forms.ImageField()
	class Meta:
		model = User
		fields = ['image']		




# class UserRegistrationForm(UserCreationForm):
# 	email = forms.EmailField()

# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'password1', 'password2']
