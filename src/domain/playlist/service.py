from src.apps.music_discovery.service import create_playlist
from src.domain.common import constants
from src.domain.playlist.commands import ProvideExternalPlaylist
from src.domain.playlist.entities import Playlist
from src.domain.playlist.errors import PlaylistExistsError
from src.libs.common_domain import aggregate_repository, dispatcher


def create_external_playlist(playlist_id, playlist_name, _aggregate_repository=None, ):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  playlist_domain_entity = _aggregate_repository.get(Playlist, playlist_id)

  if playlist_domain_entity.spotify_playlist_url:
    raise PlaylistExistsError(f'playlist: {playlist_id} already has a spotify playlist')

  playlist = create_playlist(playlist_name)
  external_url = playlist['external_urls']['spotify']

  spotify_url_command = ProvideExternalPlaylist(playlist['name'], constants.SPOTIFY, playlist['id'], external_url)

  dispatcher.send_command(playlist_id, spotify_url_command)
