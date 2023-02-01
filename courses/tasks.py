from celery import shared_task

from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponse
from .models import Course, Lesson, Video
from .utils import (
    yt_playlist_details,
    yt_playlist_videos,
    yt_video_duration,
    youtube_duration_convertion,
)


@shared_task
def create_course_from_ytplaylist():
    pass


@shared_task(bind=True)  # shared task must always be first
@transaction.atomic
def yt_playlist_create_course(self, b_user, playlist_id):
    """
    function for creating course from a youtube playlist url
    """
    print("@@@@@@@@", self.request)
    error = ""
    error_occured_at = ""
    try:
        playlist_details = yt_playlist_details(playlist_id)
        video_list = yt_playlist_videos(playlist_id)
    except Exception as e:
        error = e
        error_occured_at = "trying to get playlist details from youtube"
    else:
        try:
            course = Course.objects.create(
                author=b_user,
                title=playlist_details["title"],
                playlist=playlist_id,
                brief_description=playlist_details["description"],
                thumbnail_url=playlist_details["thumbnails"]["standard"]["url"],
                # youtube_channel=playlist_details["channelTitle"],
            )
            try:
                lesson = Lesson.objects.create(
                    course=course,
                    title="Lesson 1",
                    position=1,
                )
                try:
                    total_lesson_time = 0
                    for video in video_list:
                        video_id = video["video_id"]
                        yt_duration = yt_video_duration(video_id)
                        video_seconds, cleaned_total_time = youtube_duration_convertion(
                            yt_duration
                        )
                        Video.objects.create(
                            lesson=lesson,
                            course=course,
                            title=video["title"],
                            position=video["position"],
                            video_id=video_id,
                            duration_seconds=video_seconds,
                            duration_time=cleaned_total_time,
                        )
                        total_lesson_time += video_seconds

                    lesson.total_video_seconds = total_lesson_time
                    course.total_watch_time = total_lesson_time
                    lesson.save()
                    course.save()
                    return redirect("lesson-detail", course.id)
                except Exception as e:
                    error = e
                    error_occured_at = "trying to create video object"

            except Exception as e:
                error = e
                error_occured_at = "trying to create lesson object"

        except Exception as e:
            error = e
            error_occured_at = "trying to create course object"
    finally:
        context = {"error": error, "error_occured_at": error_occured_at}
        return render(request, "courses/playlist_form.html", context)
