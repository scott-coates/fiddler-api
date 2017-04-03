from src.apps.music_discovery import tasks
from src.apps.read_model.key_value.request.service import incr_album_promoted


def update_album_promoted(request_id, total_albums_promoted):
  albums_promoted_counter = incr_album_promoted(request_id, total_albums_promoted)

  if albums_promoted_counter == total_albums_promoted:
    tasks.update_request_playlist_task.delay(request_id)
