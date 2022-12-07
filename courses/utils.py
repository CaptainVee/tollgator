from googleapiclient.discovery import build

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
