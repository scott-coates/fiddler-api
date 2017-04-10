import logging
import webbrowser

from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.apps.read_model.key_value.request.service import process_artist_request
from src.domain.request.events import RequestSubmitted1, PlaylistRefreshedWithTracks1, ArtistPromotedToRequest1, \
  PlaylistCreatedForRequest
from src.libs.common_domain.decorators import event_idempotent

logger = logging.getLogger(__name__)


@receiver(RequestSubmitted1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  artist_names = event.data['artist_names']
  artist_ids = event.data['artist_ids']
  r_id = kwargs['aggregate_id']

  for artist_name in artist_names:
    tasks.discover_music_for_request_task.delay(r_id, artist_name)

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
  logger.info(spotify_url)
