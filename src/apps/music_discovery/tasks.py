import logging
from itertools import groupby

from django_rq import job

from src.apps.music_discovery import service
from src.domain.agreement_type import services
from src.domain.request.commands import RefreshPlaylistWithAlbum
from src.libs.common_domain import dispatcher

logger = logging.getLogger(__name__)


# @job('high')
# def create_artist_task(_aggregate_repo=None, _dispatcher=None, **kwargs):
#   if not _aggregate_repo: _aggregate_repo = aggregate_repository
#   if not _dispatcher: _dispatcher = dispatcher
#
#   agreement_id = kwargs['aggregate_id']
#
#   # check if already exists - idempotent
#   try:
#
#     # pa and agreements share same id
#     agreement = _aggregate_repo.get(Agreement, agreement_id)
#
#     logger.debug('Agreement already exists: %s', agreement_id)
#
#     return agreement.id
#
#   except ObjectDoesNotExist:
#
#     log_message = ("Create agreement task for id: %s", agreement_id)
#
#     with log_wrapper(logger.debug, *log_message):
#       data = dict({'id': agreement_id}, **kwargs['event'].data)
#       create_agreement = CreateArtist(**data)
#
#       _dispatcher.send_command(agreement_id, create_agreement)
#
#
# @job('default')
# def send_alerts_for_agreements_task():
#   # get list of agreements where the flag is enabled, not created, and date has passed
#   agreement_ids_with_due_outcome_alerts = (
#     services
#       .get_agreements_with_due_outcome_alert()
#       .values_list('id', flat=True)
#     # putting values_list here and not in service becuase my thinking is if the service returns a django object list
#     # then we can just return them. if you look at search_service, the service layer actually calls values_list but
#     # this layer is returning a custom object (it includes count, results, etc).
#   )
#
#   agreement_ids_with_due_outcome_notice_alerts = (
#     services
#       .get_agreements_with_due_outcome_notice_alert()
#       .values_list('id', flat=True)
#   )
#
#   outcome_set = set(agreement_ids_with_due_outcome_alerts)
#   outcome_notice_set = set(agreement_ids_with_due_outcome_notice_alerts)
#   ids = outcome_set.union(outcome_notice_set)
#
#   # the reason i'm doing this in one task is that i'm worried about concurrency conflicts.
#   # if we have a bunch of simultaneous tasks modifying the same instances, we could potentially overwrite bool flags
#   # which would result in multiple emails going out.
#   for ag_id in ids:
#     send_alert_for_agreement_task.delay(ag_id)
#
#
# @job('default')
# def send_alert_for_agreement_task(agreement_id, _dispatcher=None):
#   if not _dispatcher: _dispatcher = dispatcher
#   log_message = ("Send agreement alert task for id: %s", agreement_id)
#
#   with log_wrapper(logger.debug, *log_message):
#     send_alerts_command = SendAgreementAlerts()
#
#     _dispatcher.send_command(agreement_id, send_alerts_command)
#
#
# @job('high')
# def save_agreement_alert_task(agreement_id,
#                               outcome_alert_date, outcome_alert_enabled, outcome_alert_created,
#                               outcome_notice_alert_date, outcome_notice_alert_enabled, outcome_notice_alert_created,
#                               ):
#   log_message = ("Create agreement_alert task for agreement_id: %s", agreement_id)
#
#   with log_wrapper(logger.info, *log_message):
#     return services.save_agreement_alert(agreement_id,
#                                          outcome_alert_date,
#                                          outcome_alert_enabled,
#                                          outcome_alert_created,
#                                          outcome_notice_alert_date,
#                                          outcome_notice_alert_enabled,
#                                          outcome_notice_alert_created).id
#
#
# @job('high')
# def save_agreement_search_task(agreement_id, user_id, name, counterparty, agreement_type_id):
#   log_message = ("Save agreement_search task for agreement_id: %s", agreement_id)
#
#   with log_wrapper(logger.info, *log_message):
#     return services.save_agreement_search(agreement_id, user_id, name, counterparty, agreement_type_id).id
#
#
# @job('high')
# def delete_agreement_task(agreement_id):
#   log_message = ("Delete agreement_search task for agreement_id: %s", agreement_id)
#
#   with log_wrapper(logger.info, *log_message):
#     return services.delete_agreement(agreement_id)


@job('high')
def discover_music_for_request_task(request_id, artist_name):
  return service.discover_music_for_request(request_id, artist_name)


@job('high')
def discover_tracks_for_album_task(album_id, artist_id):
  return service.discover_tracks_for_album(album_id, artist_id)


@job('high')
def update_request_playlist_task(request_id, album_id):
  refresh = RefreshPlaylistWithAlbum(album_id)
  dispatcher.send_command(request_id, refresh)


@job('high')
def update_playlist_with_tracks_task(playlist_id, track_ids, ):
  return service.update_playlist_with_tracks(playlist_id, track_ids)


@job('high')
def discover_top_tracks_for_artist_task(artist_id):
  tracks = service.discover_top_tracks_for_artist(artist_id)

  albums = groupby(tracks, lambda t: t['album']['id'])

  for album_key, top_tracks in albums:
    album = list(top_tracks)[0]['album']
    album_uri = album['uri']
    album_id = service.create_album_from_spotify_uri(album_uri, artist_id)
    discover_tracks_for_album_task.delay(album_id, artist_id)

  external_track_ids = [t['id'] for t in tracks]
  add_artist_top_tracks_task.delay(artist_id, external_track_ids)


@job('high')
def add_artist_top_tracks_task(artist_id, external_track_ids, ):
  return service.add_artist_top_tracks(artist_id, external_track_ids, )
