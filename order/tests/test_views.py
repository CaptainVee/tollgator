import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user_model

from unittest.mock import patch
from decimal import Decimal

from courses.models import Course
from ..models import Order, Cart, Transaction
from ..views import enroll, checkout
from ..payments import initiate_paystack_url

User = get_user_model()


@pytest.mark.django_db
class TestOrder:
    def setup_class(cls):
        pass

    def test_enroll_view(self):
        # Create a user, course, and cart for testing
        user = User.objects.create(username="testuser")
        author = User.objects.create(username="author", email="testuser@example.com")
        course = Course.objects.create(title="Test Course", price=0, author=author)
        cart = Cart.objects.create(user=user)

        # Set up the request
        request_factory = RequestFactory()
        url = reverse("enroll", args=[course.id])
        request = request_factory.get(url)
        request.user = user

        # Test enrolling in the course
        response = enroll(request, course.id)

        # Check that the response
        assert response.status_code == 200

        # Check that the user is redirected to the correct URL

        # assert response.url == redirect_url

        # Check that an order and cart were created
        assert Order.objects.filter(user=user, course=course, ordered=False).exists()
        assert Cart.objects.filter(user=user, orders__course=course).exists()

        # # Test trying to enroll in the course again
        # response = enroll(request, course.id)

        # # Check that the response is a redirect
        # assert response.status_code == 302

        # redirect_url = reverse(
        #     "lesson-video-detail", args=[course.id, course.last_video_watched(user).id]
        # )
        # # Check that the user is redirected to the correct URL
        # assert response.url == redirect_url

        # Check that no new order or cart was created
        assert (
            Order.objects.filter(user=user, course=course, ordered=False).count() == 1
        )
        assert Cart.objects.filter(user=user, orders__course=course).count() == 1

    def test_checkout_view(self):
        # Set up test data
        user = User.objects.create_user(
            username="testuser", password="testpass", email="test@example.com"
        )
        author = User.objects.create(username="author", email="testuser@example.com")
        course = Course.objects.create(title="Test Course", price=0, author=author)
        order = Order.objects.create(user=user, course=course)
        cart = Cart.objects.create(user=user, total_amount=Decimal("10.00"))
        cart.orders.add(order)
        cart_id = cart.id
        server_url = "http://localhost:8000"

        # Set up request
        request_factory = RequestFactory()
        request = request_factory.get(reverse("checkout", args=[cart_id]))
        request.user = user

        # add middleware to the request
        middleware = SessionMiddleware(get_response=lambda r: None)
        middleware.process_request(request)
        middleware = MessageMiddleware(get_response=lambda r: None)
        middleware.process_request(request)

        # Mock paystack response
        paystack_response = {
            "data": {"authorization_url": "https://paystack.com/some/url"}
        }

        with patch(
            "order.payments.initiate_paystack_url", return_value=paystack_response
        ):
            # Call view function
            response = checkout(request, cart_id)

        # Check redirect
        assert response.status_code == 302
        # assert response.url == paystack_response["data"]["authorization_url"]

        # Check transaction was created with correct data
        transaction = Transaction.objects.get(cart=cart)
        assert transaction.transaction_ref != ""
        assert transaction.payment_provider == "payment_paystack"
        assert transaction.total_price == cart.total_amount
