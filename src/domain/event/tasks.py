import logging

from tasktiger import linear

from src.domain.event.commands import RefreshEventPlaylist
from src.libs.common_domain import dispatcher
from src.libs.job_utils.job_decorator import job

logger = logging.getLogger(__name__)


@job(queue='high', retry=True, retry_method=linear(5, 5, 10))
def refresh_event_playlist_task(request_id):
  refresh = RefreshEventPlaylist()
  dispatcher.send_command(request_id, refresh)
