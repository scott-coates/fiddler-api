import logging
import webbrowser

from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.apps.music_discovery.signals import artist_url_discovered
from src.apps.read_model.key_value.event.service import provide_journal_artist_for_event
from src.domain.common import constants
from src.domain.event.events import EventCreated1, EventPlaylistRefreshedWithTracks1, PlaylistCreatedForEvent
from src.domain.request.events import RequestSubmitted1, RequestPlaylistRefreshedWithTracks1, PlaylistCreatedForRequest
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
@receiver(RequestPlaylistRefreshedWithTracks1.event_signal)
def request_playlist_refreshed_1(**kwargs):
  event = kwargs['event']

  external_id = event.data['external_id']
  track_ids = event.data['track_ids']

  tasks.update_playlist_with_tracks_task.delay(external_id, track_ids)


@event_idempotent
@receiver(EventPlaylistRefreshedWithTracks1.event_signal)
def event_playlist_refreshed_1(**kwargs):
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


@receiver(PlaylistCreatedForEvent.event_signal)
def open_event_playlist(**kwargs):
  event = kwargs['event']

  spotify_url = event.data['external_url']
  webbrowser.open(spotify_url)
  logger.info(spotify_url)


@receiver(artist_url_discovered)
def artist_url_callback(sender, **kwargs):
  url = kwargs[constants.URL]
  attrs = kwargs[constants.ATTRS]

  tasks.discover_music_from_artist_website_and_associate_with_entity_task.delay(url, attrs)
