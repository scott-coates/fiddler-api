import django
from django.conf import settings
from django.dispatch import receiver

from src.libs.common_domain.domain_command import DomainCommand
from src.tasks import RequestSubmitted1, populate_request, ArtistCreated, create_playlist

django.setup()

# region bootstrap interact
from src.libs.common_domain import aggregate_repository
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.dispatcher import send_command
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.python_utils.objects.object_utils import initializer

request_id = generate_id()


class SubmitRequest(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, artists):
    pass


@receiver(SubmitRequest.command_signal)
def submit_request(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Request.submit(**command.data)
  _aggregate_repository.save(request, -1)


@receiver(RequestSubmitted1.event_signal)
def execute_asset_created_1(**kwargs):
  event = kwargs['event']
  request_id = kwargs['aggregate_id']
  for a in event.artists:
    populate_request.delay(request_id, a)


class Request(AggregateBase):
  @classmethod
  def submit(cls, id, artists):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artists or not all(artists):
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artists))

    return ret_val

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.artists = event.artists


class Artist(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    ret_val._raise_event(ArtistCreated(id, name))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name


class Album:
  def __init__(self, id, name, artist_id):
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not artist_id:
      raise TypeError("artist_id is required")

    self.id = id
    self.name = name
    self.artist_id = artist_id


class Track:
  def __init__(self, id, name, album_id):
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not album_id:
      raise TypeError("album_id is required")

    self.id = id
    self.name = name
    self.album_id = album_id

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name


artists = """
make war
"""

artists = list(filter(bool, artists.split('\n')))

# send_command(-1, SubmitRequest(request_id, artists))

# endregion

# region vanilla
# import spotipy
# import spotipy.util as util
#
# scope = 'playlist-modify-public'
# token = util.prompt_for_user_token('punkrockplaylist', scope, settings.SPOTIFY_CLIENT_ID,
#                                    settings.SPOTIFY_CLIENT_SECRET, 'http://localhost/')
#
# create_playlist.delay(token, 'punkrockplaylist', request_id)
#
# for artist in artists:
#   populate_request.delay(token, 'punkrockplaylist', request_id, artist)

# endregion
