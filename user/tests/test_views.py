import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "testpass123"

    def test_signup(self, client):
        signup_url = reverse("account_signup")
        response = client.get(signup_url)
        assert response.status_code == 200

        response = client.post(
            signup_url,
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        assert response.status_code == 302

        user = User.objects.get(username="testuser")
        assert user.check_password("testpass123")
        assert user.is_active

    def test_login(self, client):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass123"
        )
        login_url = reverse("account_login")
        response = client.get(login_url)
        assert response.status_code == 200

        response = client.post(
            login_url,
            {
                "login": "testuser",
                "password": "testpass123",
            },
        )
        assert response.status_code == 302

    def test_user_logout(self, client):
        response = client.get(reverse("account_logout"))
        assert response.status_code == 302

    def test_user_information_secure(self, client):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass123"
        )
        client.login(email="testuser@example.com", password="testpass123")
        response = client.get(reverse("profile"))
        assert "testuser@example.com" in response.content.decode()
