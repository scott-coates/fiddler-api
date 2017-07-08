import logging

from src.apps.read_model.key_value.event import service
from src.domain.event.tasks import refresh_event_playlist_task
from src.libs.job_utils.job_decorator import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job(queue='high')
def process_artist_event_task(event_id, artist_id):
  log_message = (
    "determine if event is ready for refresh. event id: %s. artist_id: %s.",
    event_id, artist_id
  )

  with log_wrapper(logger.debug, *log_message):
    service.process_artist_event(event_id, artist_id)

    processed_artists_count_for_event = service.get_processed_artists_for_event(event_id)
    journaled_artists_count_for_event = service.get_journaled_artists_for_event(event_id)

    intersection_count = len(
      set(processed_artists_count_for_event).intersection(set(journaled_artists_count_for_event))
    )
    logger.debug(
      "processed_artists_count_for_event: %i. journaled_artists_count_for_event: %s.",
      processed_artists_count_for_event, journaled_artists_count_for_event
    )

    if intersection_count == len(journaled_artists_count_for_event):
      logger.debug('Refresh playlist for %s.', event_id)
      refresh_event_playlist_task.delay(event_id)
