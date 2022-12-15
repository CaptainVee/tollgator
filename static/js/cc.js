var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player("player", {
    playerVars: {
      playsinline: 1,
      modestbranding: 1,
    },
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
    },
  });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
  event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
// BUFFERING, CUED, ENDED, PAUSED, PLAYING, UNSTARTED

function onPlayerStateChange(event) {
  console.log("this is an event", event);
  const currentTime = player.getCurrentTime();
  console.log(event.data);
  savePlaybackTime(currentTime, event.data, YT.PlayerState);
}

function savePlaybackTime(currentTime, eventData, playerState) {
  $.ajax({
    url: "/new/",
    type: "POST",
    data: {
      currentTime: currentTime,
      videoId: "{{ video.id }}",
      event: eventData,
      playerState: playerState,
      csrfmiddlewaretoken: "{{ csrf_token }}",
    },
    success: function (response) {
      console.log(response);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

onYouTubeIframeAPIReady();
