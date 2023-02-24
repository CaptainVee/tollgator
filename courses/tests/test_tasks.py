import pytest
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
    assert result.get() == {
        "course_pk": str(user.courses.first().pk),
        "status": "SUCCESS",
    }

    # Check that a course, lesson, and two videos were created
    assert user.courses.count() == 1
    course = user.courses.first()
    assert course.title == "Test Playlist"
    assert course.lessons.count() == 1
    lesson = course.lessons.first()
    assert lesson.title == "Lesson 1"
    assert lesson.videos.count() == 2

    # Check that the video durations were parsed correctly
    assert lesson.videos.first().duration_seconds == 5025
    assert lesson.total_video_seconds == 10050  # there are two videos here
    assert course.total_watch_time == 10050
