import logging

from src.apps.read_model.key_value.common import get_read_model_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client

logger = logging.getLogger(__name__)


def incr_artist_promoted(request_id):
  kdb = get_key_value_client()

  ret_val = kdb.hincrby(get_read_model_name('request_promoted_artists:{0}', request_id), 'counter')

  return ret_val


def incr_artists_for_request(request_id, artists_count):
  kdb = get_key_value_client()

  # this `counter` key is needed to exist for other funcs
  ret_val = kdb.hsetnx(get_read_model_name('request_promoted_artists:{0}', request_id), 'counter', 0)
  ret_val = kdb.hincrby(get_read_model_name('request_promoted_artists:{0}', request_id), 'total', artists_count)

  logger.debug('incr artists for request: %s. artists_count: %s. total: %s', request_id, artists_count, ret_val)
  return ret_val


def get_artists_count_for_request(request_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('request_promoted_artists:{0}', request_id))

  if ret_val:
    ret_val = dict(map(lambda m: (m[0].decode(), m[1].decode()), ret_val.items()))
    ret_val = {
      'total': int(ret_val['total']),
      'counter': int(ret_val['counter']),
    }

  return ret_val
