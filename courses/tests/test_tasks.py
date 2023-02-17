from celery.contrib.testing.tasks import assert_task_success, task_message
from django.test import TestCase
from unittest.mock import patch

from courses.tasks import yt_playlist_create_course


class TestYtPlaylistCreateCourseTask(TestCase):
    def test_yt_playlist_create_course_success(self):
        user_id = 1
        playlist_id = "ABC123"

        # Mock the external functions called in the task
        with patch("courses.tasks.yt_playlist_details") as mock_playlist_details, patch(
            "courses.tasks.yt_playlist_videos"
        ) as mock_playlist_videos, patch(
            "courses.tasks.yt_video_duration"
        ) as mock_video_duration, patch(
            "courses.tasks.youtube_duration_convertion"
        ) as mock_duration_conversion:

            # Set up mock return values
            mock_playlist_details.return_value = {
                "title": "Playlist Title",
                "description": "Playlist description",
                "thumbnails": {
                    "standard": {"url": "https://example.com/thumbnail.jpg"}
                },
            }
            mock_playlist_videos.return_value = [
                {"video_id": "XYZ789", "title": "Video 1", "position": 1},
                {"video_id": "DEF456", "title": "Video 2", "position": 2},
            ]
            mock_video_duration.return_value = "PT2M30S"
            mock_duration_conversion.return_value = (150, "2m 30s")

            # Call the Celery task
            result = yt_playlist_create_course.delay(user_id, playlist_id)

            # Check that the task returns "SUCCESS"
            assert_task_success(result, "SUCCESS")

            # Check that the Course, Lesson, and Video objects were created with the correct values
            message = task_message(result)
            course = message["result"]["course"]
            lesson = message["result"]["lesson"]
            videos = message["result"]["videos"]
            self.assertEqual(course.title, "Playlist Title")
            self.assertEqual(course.playlist, playlist_id)
            self.assertEqual(course.author_id, user_id)
            self.assertEqual(course.thumbnail_url, "https://example.com/thumbnail.jpg")
            self.assertEqual(course.brief_description, "Playlist description")
            self.assertEqual(course.total_watch_time, 300)
            self.assertEqual(lesson.title, "Lesson 1")
            self.assertEqual(lesson.position, 1)
            self.assertEqual(lesson.total_video_seconds, 300)
            self.assertEqual(len(videos), 2)
            self.assertEqual(videos[0].title, "Video 1")
            self.assertEqual(videos[0].position, 1)
            self.assertEqual(videos[0].duration_seconds, 150)
            self.assertEqual(videos[0].duration_time, "2m 30s")
            self.assertEqual(videos[1].title, "Video 2")
            self.assertEqual(videos[1].position, 2)
            self.assertEqual(videos[1].duration_seconds, 150)
            self.assertEqual(videos[1].duration_time, "2m 30s")
