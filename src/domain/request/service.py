from src.domain.request.commands import CreatePlaylistForRequest
from src.libs.common_domain.dispatcher import send_command


def create_spotify_playlist_for_request(request_id):
  command = CreatePlaylistForRequest()
  send_command(request_id, command)
