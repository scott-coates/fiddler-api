import logging

from django_rq import job

from src.apps.read_model.key_value.artist import service

logger = logging.getLogger(__name__)


#
# @job('default')
# def save_recent_eo_content_task(eo_id, eo_attrs, external_id, provider_type, provider_action_type, prospect_id):
#   log_message = (
#     "eo_id: %s, prospect_id: %s", eo_id, prospect_id
#   )
#
#   with log_wrapper(logger.info, *log_message):
#     return service.save_recent_eo_content(eo_id, eo_attrs, external_id, provider_type, provider_action_type,
#                                           prospect_id)
#
#
# @job('default')
# def save_recent_prospect_discovery_network_connections_from_eo_task(eo_attrs, provider_type, prospect_id):
#   log_message = (
#     "prospect_id: %s", prospect_id
#   )
#   with log_wrapper(logger.info, *log_message):
#     service.save_recent_prospect_discovery_network_connections_from_eo(eo_attrs, provider_type, prospect_id)

@job('high')
def set_album_external_id_task(album_id, release_date, provider_type, external_id):
  return service.set_album_external_id(album_id, release_date, provider_type, external_id)


@job('high')
def set_album_id_task(album_id, provider_type, external_id):
  return service.set_album_id(album_id, provider_type, external_id)


@job('high')
def set_track_external_id_task(track_id, provider_type, external_id):
  return service.set_track_external_id(track_id, provider_type, external_id)
