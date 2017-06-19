from src.apps.read_model.key_value.common import get_read_model_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def add_unique_genre_id(genre_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('genre_unique_id:{0}:{1}', provider_type, external_id), genre_id)

  return ret_val


def clear_unique_genre_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.delete(get_read_model_name('genre_unique_id:{0}:{1}', provider_type, external_id))

  return ret_val


def get_unique_genre_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('genre_unique_id:{0}:{1}', provider_type, external_id))

  return ret_val
