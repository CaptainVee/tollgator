from googleapiclient.discovery import build
from django.core.mail import EmailMessage
import cv2
import re
from datetime import time
from get_env import get_secret

youtube_api_key = get_secret("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=youtube_api_key)

hours_pattern = re.compile(r"(\d+)H")
minutes_pattern = re.compile(r"(\d+)M")
seconds_pattern = re.compile(r"(\d+)S")


def extract_playlist_link(link):
    """Extracts the playlist ID from a YouTube playlist link."""
    # Use a regular expression to find the playlist ID
    pattern = r"(?<=list=)[^&]+"
    match = re.search(pattern, link)
    if match:
        return match.group(0)
    else:
        return None


def yt_playlist_details(playlist_id):
    """
    returns the details of the youtube playlist such as title, description,
    date_published, thumbnail, channel name etc
    """
    request = youtube.playlists().list(part="snippet", id=playlist_id)

    response = request.execute()

    playlist_details = response["items"][0]["snippet"]

    return playlist_details


def yt_playlist_videos(playlist_id):
    """
    returns the list of youtube videos in a playlist as a list with the video title,
    position and video id respectively.
    example [{'title', 0, 'CkIrizsP64c'}, {'title', 1, 'CkIrizsP64c'},]
    """
    next_page_token = None
    video_details = []

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )

        response = request.execute()

        for item in response["items"]:
            new_dict = {}
            new_dict["title"] = item["snippet"]["title"]
            new_dict["position"] = item["snippet"]["position"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            new_dict["video_id"] = video_id

            video_details.append(new_dict)
            # video_details["thumbnail"] = item["snippet"]["thumbnail"]

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_details


def yt_video_duration(video_id):
    request = youtube.videos().list(part="contentDetails", id=video_id)
    response = request.execute()

    duration = response["items"][0]["contentDetails"]["duration"]

    return duration


def youtube_duration_convertion(duration):
    """
    returns a properly formatted time
    """

    hours = hours_pattern.search(duration)
    minutes = minutes_pattern.search(duration)
    seconds = seconds_pattern.search(duration)

    hours = int(hours.group(1)) if hours else 0
    minutes = int(minutes.group(1)) if minutes else 0
    seconds = int(seconds.group(1)) if seconds else 0

    video_seconds = hours * 3600 + minutes * 60 + seconds

    cleaned_total_time = time(hour=int(hours), minute=int(minutes), second=int(seconds))

    return video_seconds, cleaned_total_time


def get_transcript(video_id, course_id):
    pass
    # request = youtube.captions().list(part="snippet", videoId=video_id)
    # response = request.execute()

    # # Get the transcript of the video in English
    # for item in response["items"]:
    #     if item["snippet"]["language"] == "en":
    #         caption_id = item["id"]
    #         break
    # else:
    #     # No English transcript found
    #     return None

    # request = youtube.captions().download(id=caption_id, tfmt="srv3")
    # transcript = request.execute()

    # Save the transcript text to the Course model
    # course = Course.objects.get(id=course_id)
    # course.transcription = transcript
    # course.save()


def generate_certificates(name):
    certificate_template_image = cv2.imread("media/certificate-template.jpeg")
    saved_url = "media/{}.jpeg".format(name.strip())
    cv2.putText(
        img=certificate_template_image,
        text=name.strip(),
        org=(815, 1500),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=5,
        color=(0, 0, 250),
        thickness=5,
        lineType=cv2.LINE_AA,
    )
    cv2.imwrite(saved_url, certificate_template_image)
    return saved_url


def email_sending(to_mail, name):
    body = f""" Dear {name},
    We're excited to inform you that your course has been successfully
    created on our platform! Your course is now live and available for students to enroll.

    To access your course, simply log in to your account and navigate to your dashboard.
    From there, you can manage your course content, pricing, and enrollment options.

    We're thrilled to have you as an instructor on our platform and look forward to seeing
    the impact your course will have on our students.

    If you have any questions or concerns, please don't hesitate to reach out to our support
    team. We're always here to help.
    Best regards,

    Tollgator
    """
    try:
        message = EmailMessage(
            subject="Congratulations, your course has been successfully created!",
            body=body,
            from_email="captainvee7@gmail.com",
            to=[
                to_mail,
                "captainvee3@gmail.com",
            ],
        )
        message.send(fail_silently=False)
    except Exception:
        return False
    return True
