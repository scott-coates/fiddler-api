import logging
import webbrowser

from django.dispatch import receiver

from src.domain.playlist.events import PlaylistCreated1, ExternalPlaylistGenerated1
from src.domain.playlist.tasks import create_external_playlist_task

logger = logging.getLogger(__name__)


@receiver(PlaylistCreated1.event_signal)
def create_external_playlist_event(**kwargs):
  event = kwargs['event']

  playlist_id = kwargs['aggregate_id']
  name = event.data['name']
  create_external_playlist_task.delay(playlist_id, name)


@receiver(ExternalPlaylistGenerated1.event_signal)
def open_playlist(**kwargs):
  event = kwargs['event']

  spotify_url = event.data['external_url']
  webbrowser.open(spotify_url)
  logger.info(spotify_url)
