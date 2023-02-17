from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Course

User = get_user_model()


class CourseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        self.course_data = {
            "author": self.user,
            "playlist": "https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK",
            "title": "Test Course",
            "brief_description": "This is a test course",
            "content": "This is the content of the test course",
            "thumbnail": "test_thumbnail.jpg",
            "thumbnail_url": "https://example.com/test_thumbnail.jpg",
            "total_watch_time": 60,
            "translation": "This is a translation of the test course",
            # "price": 5.99,
            "is_private": False,
        }

        self.course = Course.objects.create(**self.course_data)

    def test_create_course(self):
        course_data = {
            "author": self.user,
            "playlist": "https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK",
            "title": "New Test Course",
            "brief_description": "This is a new test course",
            "content": "This is the content of the new test course",
            "thumbnail": "new_test_thumbnail.jpg",
            "thumbnail_url": "https://example.com/new_test_thumbnail.jpg",
            "total_watch_time": 120,
            "translation": "This is a translation of the new test course",
            # "price": 19.0,
            "is_private": True,
        }

        response = self.client.post("/courses/create/", course_data)

        self.assertEqual(response.status_code, 302)

        new_course = Course.objects.get(title="New Test Course")

        self.assertEqual(new_course.author, self.user)
        self.assertEqual(
            new_course.playlist,
            "https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK",
        )
        self.assertEqual(new_course.brief_description, "This is a new test course")
        self.assertEqual(
            new_course.content, "This is the content of the new test course"
        )
        self.assertEqual(new_course.thumbnail, "new_test_thumbnail.jpg")
        self.assertEqual(
            new_course.thumbnail_url, "https://example.com/new_test_thumbnail.jpg"
        )
        self.assertEqual(new_course.total_watch_time, 120)
        self.assertEqual(
            new_course.translation, "This is a translation of the new test course"
        )
        # self.assertEqual(new_course.price, 19.0)
        self.assertEqual(new_course.is_private, True)
