from src.domain.event.commands import CreatePlaylistForEvent
from src.libs.common_domain.dispatcher import send_command


def create_spotify_playlist_for_event(event_id):
  command = CreatePlaylistForEvent()
  send_command(event_id, command)
