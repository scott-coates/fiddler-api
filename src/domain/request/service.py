from src.domain.playlist.commands import CreatePlaylist
from src.domain.request.commands import LinkRequestToPlaylist
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id


def create_playlist_for_request(request_id):
  playlist_id = generate_id()

  create = CreatePlaylist(playlist_id, playlist_id, 'request', request_id)
  dispatcher.send_command(playlist_id, create)

  link = LinkRequestToPlaylist(playlist_id)
  dispatcher.send_command(request_id, link)

  return playlist_id
