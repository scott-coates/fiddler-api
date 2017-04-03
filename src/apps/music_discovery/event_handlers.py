from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.domain.request.events import RequestSubmitted1, AlbumAddedToRequest1, PlaylistRefreshedWithTracks1


@receiver(RequestSubmitted1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  artist_names = event.data['artist_names']
  artist_ids = event.data['artist_ids']
  r_id = kwargs['aggregate_id']

  # for artist_name in artist_names:
    # tasks.discover_music_for_request_task.delay(r_id, artist_name)

  # todo move to reequest domain
  for a_name, a_id in zip(artist_names, artist_ids):
    # i want to find most popular tracks for this artist
    # store them in their aritst profile
    tasks.discover_top_tracks_for_artist_task.delay(a_id)


# todo move to reequest domain
@receiver(AlbumAddedToRequest1.event_signal)
def add_album_1(**kwargs):
  event = kwargs['event']

  album_id = event.data['album_id']
  artist_id = event.data['artist_id']
  r_id = kwargs['aggregate_id']

  discover_tracks_task = tasks.discover_tracks_for_album_task.delay(album_id, artist_id)
  tasks.update_request_playlist_task.delay(r_id, album_id, depends_on=discover_tracks_task)


@receiver(PlaylistRefreshedWithTracks1.event_signal)
def playlist_refreshed_1(**kwargs):
  event = kwargs['event']

  provider_type = event.data['provider_type']
  external_id = event.data['external_id']
  track_ids = event.data['track_ids']

  tasks.update_playlist_with_tracks_task.delay(external_id, track_ids)


@receiver(PlaylistRefreshedWithTracks1.event_signal)
def playlist_refreshed_1(**kwargs):
  event = kwargs['event']

  provider_type = event.data['provider_type']
  external_id = event.data['external_id']
  track_ids = event.data['track_ids']

  tasks.update_playlist_with_tracks_task.delay(external_id, track_ids)
