from django.dispatch import receiver

from src.domain.playlist.commands import CreatePlaylist, ProvideExternalPlaylist
from src.domain.playlist.entities import Playlist
from src.libs.common_domain import aggregate_repository


@receiver(CreatePlaylist.command_signal)
def create_playlist(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Playlist.from_attrs(**command.data)
  _aggregate_repository.save(request, -1)


@receiver(ProvideExternalPlaylist.command_signal)
def generate_spotify_url_for_playlist(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  ag = _aggregate_repository.get(Playlist, kwargs['aggregate_id'])

  version = ag.version

  ag.set_external_playlist_info(**command.data)

  _aggregate_repository.save(ag, version)
