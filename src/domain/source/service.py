from src.apps.music_discovery import service
from src.domain.common import constants


def source_lookup(provider_type, source_type, attrs):
  # if it's a spotify playlist, lookup the playlist by uri and owner
  # then iterate through every song
  # download the album --> artist --> add to system
  #  look up album and top tracks

  if source_type == constants.PLAYLIST:
    service.discover_music_from_playlist(attrs, provider_type)
  elif source_type == constants.WEBSITE:
    service.discover_music_from_website(attrs, provider_type)
