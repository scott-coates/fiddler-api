from django.dispatch import receiver

from src.apps.read_model.key_value.artist.service import get_album_tracks
from src.domain.request.commands import SubmitArtistToRequest, SubmitRequest, RefreshPlaylist
from src.domain.request.entities import Request
from src.libs.common_domain import aggregate_repository


@receiver(SubmitRequest.command_signal)
def submit_request(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Request.submit(**command.data)
  _aggregate_repository.save(request, -1)


@receiver(SubmitArtistToRequest.command_signal)
def add_artist_request(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  ag = _aggregate_repository.get(Request, kwargs['aggregate_id'])

  version = ag.version

  ag.submit_potential_artist(**command.data)

  _aggregate_repository.save(ag, version)


@receiver(RefreshPlaylist.command_signal)
def refresh_album_request(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  ag = _aggregate_repository.get(Request, kwargs['aggregate_id'])


  version = ag.version

  ag.refresh_playlist()

  # _aggregate_repository.save(ag, version)
