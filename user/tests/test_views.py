# from django.test import TestCase

# # from allauth.account.models import EmailAddress
# from django.urls import reverse
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class UserTestCase(TestCase):
#     def setUp(self):
#         self.username = "testuser"
#         self.email = "testuser@example.com"
#         self.password = "testpass123"

#     def test_signup(self):
#         signup_url = reverse("account_signup")
#         response = self.client.get(signup_url)
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post(
#             signup_url,
#             {
#                 "username": self.username,
#                 "email": self.email,
#                 "password1": self.password,
#                 "password2": self.password,
#             },
#         )
#         self.assertEqual(response.status_code, 302)

#         user = User.objects.get(username=self.username)
#         self.assertTrue(user.check_password(self.password))
#         self.assertTrue(user.is_active)

#         # email_address = EmailAddress.objects.get(user=user)
#         # self.assertFalse(email_address.verified)
#         # self.assertEqual(email_address.email, self.email)

#     # def test_email_verification(self):
#     #     user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
#     #     email_address = EmailAddress.objects.create(user=user, email=self.email, verified=False)

#     #     verify_url = reverse('account_confirm_email', kwargs={'key': email_address.key})
#     #     response = self.client.get(verify_url)
#     #     self.assertEqual(response.status_code, 302)

#     #     email_address.refresh_from_db()
#     #     self.assertTrue(email_address.verified)

#     #     user.refresh_from_db()
#     #     self.assertTrue(user.is_active)

#     def test_login(self):
#         user = User.objects.create_user(
#             username=self.username, email=self.email, password=self.password
#         )
#         login_url = reverse("account_login")
#         response = self.client.get(login_url)
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post(
#             login_url,
#             {
#                 "login": self.username,
#                 "password": self.password,
#             },
#         )
#         self.assertEqual(response.status_code, 302)

#     def test_user_logout(self):
#         response = self.client.get(reverse("account_logout"))
#         self.assertEqual(response.status_code, 302)

#     def test_user_information_secure(self):
#         user = User.objects.create_user(
#             username=self.username, email=self.email, password=self.password
#         )
#         self.client.login(email="testuser@example.com", password="testpass123")
#         response = self.client.get(reverse("profile"))
#         self.assertContains(response, "testuser@example.com")


import pytest


def test_example():
    assert 1 == 1


from unittest.mock import patch
from django.contrib.auth import get_user_model
from courses.tasks import yt_playlist_create_course

User = get_user_model()


@pytest.mark.django_db
@patch("courses.tasks.yt_playlist_details")
@patch("courses.tasks.yt_playlist_videos")
@patch("courses.tasks.yt_video_duration")
def test_yt_playlist_create_course(mock_duration, mock_videos, mock_details):
    # Create a user
    user = User.objects.create_user(username="testuser", password="testpass")

    # Set up the mock responses
    mock_details.return_value = {
        "title": "Test Playlist",
        "description": "A test playlist",
        "thumbnails": {"standard": {"url": "https://example.com/thumbnail.jpg"}},
    }
    mock_videos.return_value = [
        {"title": "Video 1", "video_id": "abc123", "position": 1},
        {"title": "Video 2", "video_id": "def456", "position": 2},
    ]
    mock_duration.return_value = "PT1H23M45S"

    # Call the Celery task
    result = yt_playlist_create_course.apply(args=[user.id, "testplaylist"])

    # Check that the task returned "SUCCESS"
    assert result.get() == "SUCCESS"

    # Check that a course, lesson, and two videos were created
    assert user.courses.count() == 1
    course = user.courses.first()
    assert course.title == "Test Playlist"
    assert course.lessons.count() == 1
    lesson = course.lessons.first()
    assert lesson.title == "Lesson 1"
    assert lesson.videos.count() == 2

    # Check that the video durations were parsed correctly
    # assert lesson.total_video_seconds == 5025
    # assert course.total_watch_time == 5025
