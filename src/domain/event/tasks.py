import logging

from tasktiger import linear

from src.domain.event import service
from src.domain.event.commands import RefreshEventPlaylist
from src.libs.common_domain import dispatcher
from src.libs.job_utils.job_decorator import job

logger = logging.getLogger(__name__)


@job(queue='default', retry=True, retry_method=linear(5, 5, 10))
def refresh_event_playlist_task(request_id):
  refresh = RefreshEventPlaylist()
  dispatcher.send_command(request_id, refresh)


@job(queue='default')
def create_spotify_playlist_for_event_task(event_id):
  return service.create_spotify_playlist_for_event(event_id)
