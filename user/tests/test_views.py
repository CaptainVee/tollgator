from django.test import TestCase

# from allauth.account.models import EmailAddress
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "testpass123"

    def test_signup(self):
        signup_url = reverse("account_signup")
        response = self.client.get(signup_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            signup_url,
            {
                "username": self.username,
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username=self.username)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)

        # email_address = EmailAddress.objects.get(user=user)
        # self.assertFalse(email_address.verified)
        # self.assertEqual(email_address.email, self.email)

    # def test_email_verification(self):
    #     user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
    #     email_address = EmailAddress.objects.create(user=user, email=self.email, verified=False)

    #     verify_url = reverse('account_confirm_email', kwargs={'key': email_address.key})
    #     response = self.client.get(verify_url)
    #     self.assertEqual(response.status_code, 302)

    #     email_address.refresh_from_db()
    #     self.assertTrue(email_address.verified)

    #     user.refresh_from_db()
    #     self.assertTrue(user.is_active)

    def test_login(self):
        user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        login_url = reverse("account_login")
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            login_url,
            {
                "login": self.username,
                "password": self.password,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)

    def test_user_information_secure(self):
        user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        self.client.login(email="testuser@example.com", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "testuser@example.com")
