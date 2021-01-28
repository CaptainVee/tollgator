from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Post, OrderItem, Order, Address, UserProfile, Lesson
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from user.models import InstructorProfile
# from pypaystack import Transaction, Customer, Plan
from django.http import JsonResponse
from paystackapi.transaction import Transaction
from paystackapi.paystack import Paystack



import datetime
import os
import random
import string

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class PostListView(ListView):
	model = Post
	template_name = 'courses/home.html'
	context_object_name = 'post'
	ordering = ['-date_posted']
	paginate_by = 5

# class UserPostListView(ListView):
#     model = Post
#     template_name = 'courses/course_detail.html'
#     context_object_name = 'post'
#     paginate_by = 5

#     def get_queryset(self, request, username, *args, **kwargs):
#         user = get_object_or_404(InstructorProfile, user=self.kwargs.get('user'))
#         # user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(user=user).order_by('-date_posted')

class UserPostDetailView(DetailView):
    model = InstructorProfile
    template_name = 'courses/instructor_detail.html'

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'price']

    def form_valid(self, form):
        form.instance.author = get_object_or_404(InstructorProfile, user=self.request.user)
        form.save()
        return super().form_valid(form)

class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    fields = ['title', 'description', 'video', 'position']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.course = get_object_or_404(Post, pk = self.kwargs.get('course_pk'))
        form.save()
        return super().form_valid(form)

class LessonDetailView(DetailView):
    model = Lesson

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'video']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class LessonDetailView(LoginRequiredMixin, View):

    def get(self, request, course_pk, lesson_pk, *args, **kwargs):
        course_qs = Post.objects.filter(pk=course_pk)
        if course_qs.exists():
            course = course_qs.first()

        lesson_qs = course.lessons.filter(pk=lesson_pk)
        if lesson_qs.exists():
            lesson = lesson_qs.first()            

        context = {'object': lesson}

        return render(request, "courses/lesson_detail.html", context)




def about(request):
	return render(request, 'courses/about.html', {'title': 'About'})

# Create your views here.

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'courses/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

def PaymentView(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, ordered=False)
        # items = order.orderitem_set.all()
        # cartItems = order.get_cart_items
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
                    'order':order,
                    'pk_public' : settings.PAYSTACK_PUBLIC_KEY

                }
    return render(request, 'courses/checkout.html', context)


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Post, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Post, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("post-detail", pk = pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("post-detail", pk = pk)


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("post-detail", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("post-detail", pk=pk)


class VerifyView(View):
    def get(self, request, id, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

        # transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY )
        # response = transaction.verify(id)
        transaction = paystack.transaction.initialize(reference=id,
                                  amount='amount', email='email')
        response = paystack.transaction.verify(reference=id)
        data = JsonResponse(response, safe=False)
        # assign the payment to the order

        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.ref_code = create_ref_code()
        order.save()

        return render(request, 'courses/verify.html', {'title': 'verify'})

class StartDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=True)
        # order_items = order.first().items.all()
        if order.exists()
            for order_item in order:
                order_items = order_item.items.all()
                context = {
                    'object': order_items
                }
                return render(self.request, 'courses/start.html', context)
        else:
            return render(self.request, 'courses/start.html', {'object' : None})
        # lesson_qs = course.lessons.filter(pk=lesson_pk)
        # if lesson_qs.exists():
        #     lesson = lesson_qs.first()            
