import webbrowser

from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.domain.request.events import RequestSubmitted1, PlaylistRefreshedWithTracks1, AlbumPromotedToRequest1, \
  PlaylistCreatedForRequest


@receiver(RequestSubmitted1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  artist_names = event.data['artist_names']
  artist_ids = event.data['artist_ids']
  r_id = kwargs['aggregate_id']

  for artist_name in artist_names:
    tasks.discover_music_for_request_task.delay(r_id, artist_name)


# todo move to reequest domain
@receiver(AlbumPromotedToRequest1.event_signal)
def add_album_1(**kwargs):
  event = kwargs['event']

  album_id = event.data['album_id']
  artist_id = event.data['artist_id']

  tasks.discover_tracks_for_album_task.delay(album_id, artist_id)


@receiver(PlaylistRefreshedWithTracks1.event_signal)
def playlist_refreshed_1(**kwargs):
  event = kwargs['event']

  provider_type = event.data['provider_type']
  external_id = event.data['external_id']
  track_ids = event.data['track_ids']

  tasks.update_playlist_with_tracks_task.delay(external_id, track_ids)


@receiver(PlaylistCreatedForRequest.event_signal)
def open_playlist(**kwargs):
  event = kwargs['event']

  spotify_url = event.data['external_url']
  webbrowser.open(spotify_url)
