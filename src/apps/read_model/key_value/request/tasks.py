import logging

from src.apps.music_discovery.tasks import refresh_request_playlist_task
from src.apps.read_model.key_value.request import service
from src.apps.read_model.key_value.request.service import get_processed_artists_count_for_request, \
  get_journaled_artists_count_for_request
from src.libs.job_utils.job_decorator import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job(queue='high')
def process_artist_request_task(request_id, artist_id):
  log_message = ("determine if request is ready for refresh. request id: %s. artist_id: %s", request_id, artist_id)

  with log_wrapper(logger.debug, *log_message):
    service.process_artist_request(request_id, artist_id)

    processed_artists_count_for_request = get_processed_artists_count_for_request(request_id)
    journaled_artists_count_for_request = get_journaled_artists_count_for_request(request_id)

    if processed_artists_count_for_request == journaled_artists_count_for_request:
      refresh_request_playlist_task.delay(request_id)
