from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.domain.request.events import RequestSubmitted1, AlbumAddedToRequest1


@receiver(RequestSubmitted1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  artists = event.data['artists']
  r_id = kwargs['aggregate_id']

  for artist_name in artists:
    tasks.discover_music_for_request_task.delay(r_id, artist_name)

@receiver(AlbumAddedToRequest1.event_signal)
def add_album_1(**kwargs):
  event = kwargs['event']

  album_id = event.data['album_id']
  r_id = kwargs['aggregate_id']

  tasks.discover_tracks_for_album_task.delay(album_id)
  # todo chain add to reqeust
