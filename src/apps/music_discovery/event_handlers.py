import logging
import webbrowser

from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.apps.music_discovery.signals import artist_url_discovered
from src.domain.common import constants
from src.domain.request.events import RequestSubmitted1, PlaylistRefreshedWithTracks1, PlaylistCreatedForRequest
from src.libs.common_domain.decorators import event_idempotent

logger = logging.getLogger(__name__)


@receiver(RequestSubmitted1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  artist_names = event.data['artist_names']
  r_id = kwargs['aggregate_id']

  for artist_name in artist_names:
    tasks.discover_music_for_request_task.delay(r_id, artist_name)


@event_idempotent
@receiver(PlaylistRefreshedWithTracks1.event_signal)
def playlist_refreshed_1(**kwargs):
  event = kwargs['event']

  external_id = event.data['external_id']
  track_ids = event.data['track_ids']

  tasks.update_playlist_with_tracks_task.delay(external_id, track_ids)


@receiver(PlaylistCreatedForRequest.event_signal)
def open_playlist(**kwargs):
  event = kwargs['event']

  spotify_url = event.data['external_url']
  webbrowser.open(spotify_url)
  logger.info(spotify_url)


@receiver(artist_url_discovered)
def artist_url_callback(sender, **kwargs):
  url = kwargs[constants.URL]

  tasks.discover_music_from_artist_website_task.delay(url)
