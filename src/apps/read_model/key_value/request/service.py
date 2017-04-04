from src.apps.read_model.key_value.common import get_read_model_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def incr_album_promoted(request_id, total_albums_promoted):
  kdb = get_key_value_client()

  kdb.hsetnx(get_read_model_name('request_promoted_albums:{0}', request_id), 'total_albums_promoted',
             total_albums_promoted)

  kdb.hsetnx(get_read_model_name('request_promoted_albums:{0}', request_id), 'counter', 0)

  ret_val = kdb.hincrby(get_read_model_name('request_promoted_albums:{0}', request_id), 'counter')

  return ret_val
