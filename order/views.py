from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Order, Pricing
from courses.models import Course
from common.utils import get_or_none

# Create your views here.


def enroll(request, course_slug):
    """
    allows users to enroll or a free course
    """
    course = get_object_or_404(Course, slug=course_slug)
    order = Order.objects.select_related("course").filter(
        course=course, user=request.user
    )
    if order:
        messages.info(request, "you have already enrolled for this course.")
    else:
        order = Order(user=request.user, course=course)
        order.save()
        messages.success(request, "You have successfully enrolled for this course.")

    return redirect("lesson-video-detail", course_slug)


# def is_valid_form(values):
#     valid = True
#     for field in values:
#         if field == "":
#             valid = False
#     return valid


# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {"object": order}
#             return render(self.request, "courses/order_summary.html", context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("/")


# def PaymentView(request):
#     if request.user.is_authenticated:
#         # items = order.orderitem_set.all()
#         # cartItems = order.get_cart_items
#         order = Order.objects.get(user=request.user, ordered=False)
#         context = {"order": order, "pk_public": settings.PAYSTACK_PUBLIC_KEY}
#     return render(request, "courses/checkout.html", context)


# @login_required
# def add_to_cart(request, pk):
#     item = get_object_or_404(Course, pk=pk)
#     order_item, created = OrderItem.objects.get_or_create(
#         item=item, user=request.user, ordered=False
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("order-summary")
#         else:
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("order-summary")
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("order-summary")


# @login_required
# def remove_from_cart(request, pk):
#     item = get_object_or_404(Post, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item, user=request.user, ordered=False
#             )[0]
#             order.items.remove(order_item)
#             order_item.delete()
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("post-detail", pk=pk)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("post-detail", pk=pk)


# @login_required
# def remove_single_item_from_cart(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item, user=request.user, ordered=False
#             )[0]
#             if order_item.quantity > 1:
#                 order_item.quantity -= 1
#                 order_item.save()
#             else:
#                 order.items.remove(order_item)
#             messages.info(request, "This item quantity was updated.")
#             return redirect("order-summary")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("post-detail", pk=pk)
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("post-detail", pk=pk)


# class VerifyView(View):
#     def get(self, request, id, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

#         # transaction = Transaction(authorization_key= settings.PAYSTACK_SECRET_KEY )
#         # response = transaction.verify(id)
#         transaction = paystack.transaction.initialize(
#             reference=id, amount="amount", email="email"
#         )
#         response = paystack.transaction.verify(reference=id)
#         data = JsonResponse(response, safe=False)
#         # assign the payment to the order

#         order_items = order.items.all()
#         order_items.update(ordered=True)
#         for item in order_items:
#             item.save()

#         order.ordered = True
#         order.ref_code = create_ref_code()
#         order.save()

#         return render(request, "courses/verify.html", {"title": "verify"})


# class StartDetailView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         order = OrderItem.objects.filter(user=self.request.user, ordered=True)
#         if order.exists():
#             context = {"object": order}
#             return render(self.request, "courses/start.html", context)
#         else:
#             return render(self.request, "courses/start.html", {"object": None})
#         # lesson_qs = course.lessons.filter(pk=lesson_pk)
#         # if lesson_qs.exists():
#         #     lesson = lesson_qs.first()
