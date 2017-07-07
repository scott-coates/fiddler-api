import logging

from src.libs.job_utils.service import get_journaled_items_for_job, get_processed_items_for_job, \
  provide_journal_items_for_job, process_items_for_job

logger = logging.getLogger(__name__)


def _get_job_key(event_id):
  return f"event:{event_id}"


def process_artist_event(event_id, artist_id):
  ret_val = process_items_for_job(_get_job_key(event_id), artist_id)

  return ret_val


def get_processed_artists_for_event(event_id):
  ret_val = get_processed_items_for_job(_get_job_key(event_id))

  return ret_val


def provide_journal_artist_for_event(event_id, artist_id):
  ret_val = provide_journal_items_for_job(_get_job_key(event_id), [artist_id])

  return ret_val


def get_journaled_artists_for_event(event_id):
  ret_val = get_journaled_items_for_job(_get_job_key(event_id))

  return ret_val
