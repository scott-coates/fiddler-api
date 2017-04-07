import logging

from src.apps.read_model.key_value.common import get_read_model_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client

logger = logging.getLogger(__name__)


def process_artist_request(request_id, artist_id):
  kdb = get_key_value_client()

  ret_val = kdb.sadd(get_read_model_name('request_processed_artists:{0}', request_id), artist_id)

  return ret_val


def provide_journal_artists_for_request(request_id, artist_ids):
  kdb = get_key_value_client()

  ret_val = kdb.sadd(get_read_model_name('request_journal_artists:{0}', request_id), *artist_ids)

  return ret_val


def get_processed_artists_count_for_request(request_id):
  kdb = get_key_value_client()

  ret_val = kdb.smembers(get_read_model_name('request_processed_artists:{0}', request_id))

  if ret_val:
    ret_val = len(ret_val)

  return ret_val


def get_journaled_artists_count_for_request(request_id):
  kdb = get_key_value_client()

  ret_val = kdb.smembers(get_read_model_name('request_journal_artists:{0}', request_id))

  if ret_val:
    ret_val = len(ret_val)

  return ret_val
