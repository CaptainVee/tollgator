import os
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Order, Cart, Transaction
from courses.models import Course
from common.utils import get_or_none, my_random_string, convert_currency_to_local
from django.contrib.auth.decorators import login_required
from .payments import verify_transaction, initiate_paystack_url


# Create your views here.


@login_required
@transaction.atomic
def enroll(request, course_id):
    """
    allows users to enroll or a free course
    """
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    try:
        order = Order.objects.get(user=user, course=course, ordered=True)

        messages.info(request, "you have already enrolled for this course.")

        return redirect(
            "lesson-video-detail", course.id, course.last_video_watched(request.user).id
        )

    except Order.DoesNotExist:
        order, created = Order.objects.get_or_create(
            user=user, course=course, ordered=False
        )
        if created:
            ref = my_random_string()
            cart = Cart.objects.create(
                reference=ref, total_amount=course.price, user=user
            )
            cart.orders.add(order)
        else:
            cart = order.cart_set.all()[0]
        local_price = convert_currency_to_local(
            user.currency, course.currency, cart.total_amount
        )
        context = {"cart": cart, "course": course, "local_price": local_price}

        return render(request, "order/checkout.html", context)


def checkout(request, cart_id):
    ref = my_random_string()
    cart = get_object_or_404(Cart, id=cart_id)
    transaction, created = Transaction.objects.update_or_create(
        cart=cart,
        defaults={
            "transaction_ref": ref,
            "payment_provider": "payment_paystack",
            "total_price": cart.total_amount,
        },
    )
    server_url = os.environ.get("SERVER_URL")  # eg localhost:8000
    email = cart.user.email
    amount = convert_currency_to_local(
        user_currency=cart.user.currency,
        product_currency="USD",
        product_amount=cart.total_amount,
    )
    currency = cart.user.currency
    callback_url = f"{server_url}/order/verify/transaction/{transaction.id}"
    response = initiate_paystack_url(
        email=email,
        amount=amount,
        transaction_ref=ref,
        currency=currency,
        callback_url=callback_url,
    )
    print(response)
    try:
        paystack_url = response["data"]["authorization_url"]
    except:
        return HttpResponse(response["message"])
    return redirect(paystack_url)


def verify(request, transaction_id):
    transaction_ref = request.GET.get("trxref")
    transaction = get_object_or_404(
        Transaction, id=transaction_id, transaction_ref=transaction_ref
    )
    response = verify_transaction(transaction_ref=transaction_ref)

    if response["status"] == True:
        status = response["data"]["status"]
        message = response["data"]["gateway_response"]
        if status == "success":
            transaction.transaction_status = "Payment Completed"
            transaction.transaction_description = message
            transaction.save()

            for order in transaction.cart.orders.all().select_related("course"):
                order.ordered = True
                order.save()
                request.user.user_dashboard.courses.add(order.course)
            messages.success(request, f"Your transaction was a {message}")
        elif status == "failed":
            transaction.transaction_status = "Payment Failed"
            transaction.transaction_description = message
            transaction.save()
            messages.error(request, f"Your transaction {message}")
    elif response["status"] == False:
        transaction.transaction_status = "Payment Error"
        transaction.transaction_description = (
            "something went wrong with the payment, contact custumer support"
        )
        transaction.save()

    return redirect("dashboard")


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
