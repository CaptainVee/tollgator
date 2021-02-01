from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import InstructorProfile
from django.db.models.signals import post_save
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Post(models.Model):
	title = models.CharField(max_length=150 )
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	label = models.CharField(choices=LABEL_CHOICES, max_length=1)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(InstructorProfile, on_delete= models.CASCADE)
	free = models.BooleanField(default=False)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True)
	image = models.ImageField(default='default.jpg', null=True, blank=True)



	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk' : self.pk}) #also known as product

	def get_add_to_cart_url(self):
		return reverse("add-to-cart", kwargs={'pk': self.pk})

	def get_remove_from_cart_url(self):
		return reverse("remove-from-cart", kwargs={'pk': self.pk})
	@property
	def lessons(self):
		return self.lesson_set.all().order_by('position')

class Lesson(models.Model):
	title = models.CharField(max_length=120)
	course = models.ForeignKey(Post, on_delete=models.CASCADE)
	video = models.FileField(default='default.mp4', upload_to='videos/')
	position = models.IntegerField()
	description = models.TextField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):

		return reverse('lesson-detail',
			kwargs={'course_pk':self.course.pk, 'lesson_pk':self.pk})




class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	one_click_purchasing = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username




class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
    	return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
    	return self.quantity * self.item.price

    def get_total_discount_item_price(self):
    	return self.quantity * self.item.discount_price

    def get_amount_saved(self):
    	return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
    	if self.item.discount_price:
    		return self.get_total_discount_item_price()
    	return self.get_total_item_price()

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ref_code = models.CharField(max_length=20, blank=True, null=True)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	being_delivered = models.BooleanField(default=False)
	received = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

 
    # 1. Item added to cart
    # 2. Adding a billing address
    # (Failed checkout)
    # 3. Payment
    # (Preprocessing, processing, packaging etc.)
    # 4. Being delivered
    # 5. Received
    # 6. Refunds
  

	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class Address(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=100)
	apartment_address = models.CharField(max_length=100)
	country = CountryField(multiple=False)
	zip = models.CharField(max_length=100)
	address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
	default = models.BooleanField(default=False)

	def __str__(self):
	    return self.user.username

	class Meta:
	    verbose_name_plural = 'Addresses'

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=User)
