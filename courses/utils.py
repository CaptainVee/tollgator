from googleapiclient.discovery import build


def youtube_playlist(playlist_id):
    api_key = ""
    video_id_list = []
    video_id_string = ""

    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.playlistItems().list(
        part="contentDetails", playlistId=playlist_id
    )
    response = request.execute()

    for item in response["items"]:
        video_id_list.append(item["contentDetails"]["videoId"])

    video_id_string = ",".join(video_id_list)

    return video_id_list


# def youtube_video(video_ids):
#     api_key = ""
#     youtube = build("youtube", "v3", developerKey=api_key)

#     request = youtube.videos().list(part="contentDetails", id=video_ids)
#     response = request.execute()

#     duration_list = []
#     for item in response["items"]:
#         duration = item["contentDetails"]["duration"]
#         duration_list.append(duration)

#     print(duration_list)
#     pass
