from django.dispatch import receiver

from src.apps.read_model.key_value.artist.service import add_unique_artist_id, clear_unique_artist_id
from src.domain.artist.commands import CreateArtist, CreateAlbum, AddTracks
from src.domain.artist.entities import Artist
from src.domain.artist.errors import DuplicateArtistError
from src.libs.common_domain import aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id


@receiver(CreateArtist.command_signal)
def create_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  newly_added = add_unique_artist_id(kwargs['aggregate_id'], command.data['provider_type'], command.data['external_id'])

  if not newly_added: raise DuplicateArtistError('artist: ', command.id, 'already exists.')

  try:
    artist = Artist.from_attrs(**command.data)
    _aggregate_repository.save(artist, -1)
  except:
    clear_unique_artist_id(command.data['provider_type'], command.data['external_id'])
    raise


@receiver(CreateAlbum.command_signal)
def create_album(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  ag = _aggregate_repository.get(Artist, kwargs['aggregate_id'])

  version = ag.version

  ag.add_album(**command.data)

  _aggregate_repository.save(ag, version)


@receiver(AddTracks.command_signal)
def add_tracks_album(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  tracks = command.data['tracks']

  ag = _aggregate_repository.get(Artist, kwargs['aggregate_id'])
  version = ag.version

  for t in tracks:
    track_id = generate_id()
    ag.add_track(id=track_id, **t)

  _aggregate_repository.save(ag, version)

#
# @receiver(UpdateAgreementAttrs.command_signal)
# def update_agreement(_aggregate_repository=None, **kwargs):
#   if not _aggregate_repository: _aggregate_repository = aggregate_repository
#
#   command = kwargs['command']
#   id = kwargs['aggregate_id']
#
#   data = command.__dict__
#
#   ag = _aggregate_repository.get(Agreement, id)
#
#   version = ag.version
#
#   ag.update_attrs(**data)
#
#   _aggregate_repository.save(ag, version)
#
#
# @receiver(SendAgreementAlerts.command_signal)
# def send_agreement_alerts(_aggregate_repository=None, **kwargs):
#   if not _aggregate_repository: _aggregate_repository = aggregate_repository
#
#   id = kwargs['aggregate_id']
#
#   ag = _aggregate_repository.get(Agreement, id)
#
#   version = ag.version
#
#   ag.send_outcome_alert_if_due()
#   ag.send_outcome_notice_alert_if_due()
#
#   _aggregate_repository.save(ag, version)
#
#
# @receiver(DeleteAgreement.command_signal)
# def delete_agreement(_aggregate_repository=None, **kwargs):
#   if not _aggregate_repository: _aggregate_repository = aggregate_repository
#
#   id = kwargs['aggregate_id']
#
#   ag = _aggregate_repository.get(Agreement, id)
#
#   version = ag.version
#
#   ag.mark_deleted()
#
#   _aggregate_repository.save(ag, version)
#
#
# @receiver(DeleteArtifact.command_signal)
# def delete_artifact(_aggregate_repository=None, **kwargs):
#   if not _aggregate_repository: _aggregate_repository = aggregate_repository
#
#   id = kwargs['aggregate_id']
#
#   command = kwargs['command']
#
#   ag = _aggregate_repository.get(Agreement, id)
#
#   version = ag.version
#
#   ag.delete_artifact(command.artifact_id)
#
#   _aggregate_repository.save(ag, version)
#
#
# @receiver(CreateArtifact.command_signal)
# def add_artifact(_aggregate_repository=None, **kwargs):
#   if not _aggregate_repository: _aggregate_repository = aggregate_repository
#
#   id = kwargs['aggregate_id']
#
#   command = kwargs['command']
#
#   ag = _aggregate_repository.get(Agreement, id)
#
#   version = ag.version
#
#   ag.create_artifact(command.artifact_id)
#
#   _aggregate_repository.save(ag, version)
