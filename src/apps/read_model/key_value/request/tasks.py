import logging

from src.apps.music_discovery.tasks import refresh_request_playlist_task
from src.apps.read_model.key_value.request import service
from src.apps.read_model.key_value.request.service import get_artists_count_for_request
from src.libs.job_utils.job_decorator import job

logger = logging.getLogger(__name__)


@job(queue='high')
def incr_artist_promoted_task(request_id):
  inc = service.incr_artist_promoted(request_id)
  artists_count_for_request = get_artists_count_for_request(request_id)

  if artists_count_for_request['total'] == artists_count_for_request['counter']:
    refresh_request_playlist_task.delay(request_id)
