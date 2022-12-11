from googleapiclient.discovery import build
import uuid
from django.core.mail import EmailMessage
import cv2

api_key = ""
youtube = build("youtube", "v3", developerKey=api_key)


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
    position and video id respectively. example ['title', 0, 'CkIrizsP64c'],
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
            new_dict["video_id"] = item["snippet"]["resourceId"]["videoId"]
            video_details.append(new_dict)
            # video_details["thumbnail"] = item["snippet"]["thumbnail"]

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_details


def yt_video_details(video_ids):
    api_key = ""
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.videos().list(part="contentDetails", id=video_ids)
    response = request.execute()

    duration_list = []
    for item in response["items"]:
        duration = item["contentDetails"]["duration"]
        duration_list.append(duration)

    print(duration_list)
    pass


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.lower()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    # usage  = '%s-%s'%('TR',my_random_string(6))
    return random[0:string_length]  # Return the random string.


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


def email_sending(to_mail, firstname, lastname, location, time, ref):
    body = f"""Hello {firstname}, {lastname}This is a confirmation of your ticket for Hilltop Encounters 2022
    Ticket Summary
    IN-PERSON CONFERENCE
    Time: {time}
    Location: {location}

    The Printable PDF ticket has been attached to this mail.

    Note: Remember to either have a printed copy or a downloaded copy of the ticket when going for the event as you might need to present it for Confirmation and or Check-in.
    Going with Friends is fun

    Let your friends know you are going
    """
    try:
        message = EmailMessage(
            subject="Here is your ticket for Hilltop Encounters 2022",
            body=body,
            from_email="captainvee7@gmail.com",
            to=[
                to_mail,
                "captainvee3@gmail.com",
            ],
        )
        message.attach_file(f"media/{firstname}-{ref}.jpg")
        message.send(fail_silently=False)
    except:
        return False
    return True
