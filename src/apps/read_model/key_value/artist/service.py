import json

from src.apps.read_model.key_value.common import get_read_model_name
from src.libs.datetime_utils.datetime_parser import get_datetime
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def add_unique_artist_id(artist_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('artist_unique_id:{0}:{1}', provider_type, external_id), artist_id)

  return ret_val


def clear_unique_artist_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.delete(get_read_model_name('artist_unique_id:{0}:{1}', provider_type, external_id))

  return ret_val


def get_unique_artist_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('artist_unique_id:{0}:{1}', provider_type, external_id))

  return ret_val


def add_unique_track_id(track_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('track_unique_id:{0}:{1}', provider_type, external_id), track_id)

  return ret_val


def get_unique_track_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('track_unique_id:{0}:{1}', provider_type, external_id))

  return ret_val


def add_external_artist_id(artist_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('artist_external_id:{0}:{1}', artist_id, provider_type, ), external_id)

  return ret_val


def get_external_artist_id(artist_id, provider_type):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('artist_external_id:{0}:{1}', artist_id, provider_type))

  return ret_val


def get_album_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('album_external_id:{0}:{1}', provider_type, external_id))

  return ret_val


def set_album_id(album_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('album_external_id:{0}:{1}', provider_type, external_id), album_id)

  return ret_val


def set_album_info(album_id, name, popularity, release_date, provider_type, external_id):
  kdb = get_key_value_client()
  data = {
    'name': name, 'popularity': popularity,
    'release_date': release_date, 'provider_type': provider_type, 'external_id': external_id
  }

  ret_val = kdb.hmset(get_read_model_name('album_info:{0}', album_id), data)

  return ret_val


def get_album_info(album_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('album_info:{0}', album_id))

  if ret_val:
    ret_val['release_date'] = get_datetime(ret_val['release_date'])
    ret_val['id'] = album_id

  return ret_val


def add_album_to_artist(album_id, artist_id):
  kdb = get_key_value_client()

  ret_val = kdb.sadd(get_read_model_name('artist_album_info:{0}', artist_id), album_id)

  return ret_val


def get_artist_albums(artist_id):
  kdb = get_key_value_client()

  ret_val = kdb.smembers(get_read_model_name('artist_album_info:{0}', artist_id))

  return ret_val


def set_track_external_id(track_id, provider_type, external_id):
  kdb = get_key_value_client()
  data = {'provider_type': provider_type, 'external_id': external_id}

  ret_val = kdb.hmset(get_read_model_name('track_external_info:{0}', track_id), data)

  return ret_val


def get_track_external_id(track_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('track_external_info:{0}', track_id))

  return ret_val


def add_track_to_album(album_id, track_data):
  kdb = get_key_value_client()

  ret_val = kdb.smembers(get_read_model_name('album_tracks_ids:{0}', album_id))

  track_id = track_data['id']

  if track_id not in ret_val:
    payload = json.dumps(track_data)
    ret_val = kdb.lpush(get_read_model_name('album_track_info:{0}', album_id), payload)

    kdb.sadd(get_read_model_name('album_tracks_ids:{0}', album_id), track_id)

  return ret_val


def get_album_tracks(album_id):
  kdb = get_key_value_client()

  ret_val = kdb.lrange(get_read_model_name('album_track_info:{0}', album_id), 0, -1) or None

  if ret_val:
    ret_val = [json.loads(r) for r in ret_val]
    ret_val = {'id': album_id, 'tracks': ret_val}

  return ret_val


def save_artist_info(artist_id, genres, popularity):
  kdb = get_key_value_client()
  genres_json = json.dumps(genres)
  data = {'genres': genres_json, 'popularity': popularity}

  ret_val = kdb.hmset(get_read_model_name('artist_info:{0}', artist_id), data)

  return ret_val


def save_artist_top_tracks(artist_id, track_data):
  kdb = get_key_value_client()

  tracks_json = json.dumps(track_data)
  ret_val = kdb.hset(get_read_model_name('artist_info:{0}', artist_id), 'top_tracks', tracks_json)

  return ret_val


def get_artist_info(artist_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('artist_info:{0}', artist_id))

  if ret_val:
    ret_val = {
      'id': artist_id,
      'genres': set(json.loads(ret_val['genres'])),
      'top_tracks': json.loads(ret_val['top_tracks']),
      'popularity': int(ret_val['popularity'])
    }

  return ret_val


def save_track_info(track_id, track_data, album_id):
  kdb = get_key_value_client()

  track_data_copy = track_data.copy()

  del track_data_copy['id']
  del track_data_copy['provider_type']
  del track_data_copy['external_id']

  track_data_copy['album_id'] = album_id
  track_data_copy['features'] = json.dumps(track_data_copy['features'])
  track_data_copy['analysis'] = json.dumps(track_data_copy['analysis'])

  ret_val = kdb.hmset(get_read_model_name('track_info:{0}', track_id), track_data_copy)

  return ret_val


# todo still needed?
def get_track_info(track_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('track_info:{0}', track_id))
  ret_val['features'] = json.loads(ret_val['features'])
  ret_val['analysis'] = json.loads(ret_val['analysis'])
  ret_val['id'] = track_id

  return ret_val
