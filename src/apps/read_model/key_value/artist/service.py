import json

from src.apps.read_model.key_value.common import get_read_model_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def add_unique_artist_id(artist_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('artist_external_id:{0}:{1}', provider_type, external_id), artist_id)

  return ret_val


def clear_unique_artist_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.delete(get_read_model_name('artist_external_id:{0}:{1}', provider_type, external_id))

  return ret_val


def get_unique_artist_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('artist_external_id:{0}:{1}', provider_type, external_id))

  if ret_val:
    ret_val = ret_val.decode()

  return ret_val


def get_album_id(provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.get(get_read_model_name('album_external_id:{0}:{1}', provider_type, external_id))

  if ret_val:
    ret_val = ret_val.decode()

  return ret_val


def set_album_id(album_id, provider_type, external_id):
  kdb = get_key_value_client()

  ret_val = kdb.setnx(get_read_model_name('album_external_id:{0}:{1}', provider_type, external_id), album_id)

  return ret_val


def set_album_external_id(album_id, release_date, provider_type, external_id):
  kdb = get_key_value_client()
  data = {'release_date': release_date, 'provider_type': provider_type, 'external_id': external_id}

  ret_val = kdb.hmset(get_read_model_name('album_external_info:{0}', album_id), data)

  return ret_val


def get_album_external_id(album_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('album_external_info:{0}', album_id))

  if ret_val:
    ret_val = dict(map(lambda m: (m[0].decode(), m[1].decode()), ret_val.items()))

  return ret_val


def set_track_external_id(track_id, provider_type, external_id):
  kdb = get_key_value_client()
  data = {'provider_type': provider_type, 'external_id': external_id}

  ret_val = kdb.hmset(get_read_model_name('track_external_info:{0}', track_id), data)

  return ret_val


def get_track_external_id(track_id):
  kdb = get_key_value_client()

  ret_val = kdb.hgetall(get_read_model_name('track_external_info:{0}', track_id))

  if ret_val:
    ret_val = dict(map(lambda m: (m[0].decode(), m[1].decode()), ret_val.items()))

  return ret_val


def add_track_to_album(album_id, track_data):
  kdb = get_key_value_client()
  ret_val = None

  existing_tracks = list(map(lambda m: m.decode(), kdb.smembers(get_read_model_name('album_tracks:{0}', album_id))))

  track_id = track_data['id']

  if track_id not in existing_tracks:
    payload = json.dumps(track_data)
    ret_val = kdb.lpush(get_read_model_name('album_data:{0}', album_id), payload)

    kdb.sadd(get_read_model_name('album_tracks:{0}', album_id), track_id)

  return ret_val


def get_album_data(album_id):
  kdb = get_key_value_client()

  ret_val = kdb.lrange(get_read_model_name('album_data:{0}', album_id), 0, -1) or None

  if ret_val:
    ret_val = [json.loads(x.decode()) for x in ret_val]
    ret_val = {'id': album_id, 'tracks': ret_val}

  return ret_val

#
# def save_recent_prospect_discovery_network_connections_from_eo(eo_attrs, provider_type, prospect_id):
#   ret_val = []
#
#   should_add_to_discovery_network = False
#
#   if provider_type == constants.Provider.TWITTER:
#
#     retweet_status = eo_attrs[constants.IS_RETWEET]
#
#     if not retweet_status:
#       should_add_to_discovery_network = True
#
#   if should_add_to_discovery_network:
#
#     mentions = eo_attrs.get(constants.MENTIONS)
#     if mentions:
#
#       recent_discovery_network = get_recent_prospect_discovery_network(prospect_id)
#
#       for mention in mentions:
#         external_id = mention[constants.EXTERNAL_ID]
#
#         existing_recent_connection = next(
#             (r for r in recent_discovery_network if
#              r[constants.EXTERNAL_ID] == external_id and r[constants.PROVIDER_TYPE] == provider_type
#              ), None)
#
#         if existing_recent_connection is None:
#           # only add new, distinct connections
#
#           payload = {
#             constants.EXTERNAL_ID: external_id,
#             constants.PROVIDER_TYPE: provider_type,
#           }
#
#           payload_str = json.dumps(payload)
#           ret_val.append(
#               push_latest(get_read_model_name('prospect_recent_discovery_network:{0}', prospect_id), payload_str, 100)
#           )
#
#   return ret_val
#
#
# def get_recent_prospect_discovery_network(prospect_id):
#   kdb = get_key_value_client()
#
#   redis_range = kdb.lrange(get_read_model_name('prospect_recent_discovery_network:{0}', prospect_id), 0, -1)
#
#   ret_val = [json.loads(x.decode()) for x in redis_range]
#
#   return ret_val
