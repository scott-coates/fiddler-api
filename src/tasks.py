import functools

from django_rq import job

from src import music
from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer
from src.music import add_rel_artist_to_playlist


@job('high')
def create_playlist(token, username, playlist_name):
  return music.create_playlist(token, username, playlist_name)


@job('high')
def populate_request(token,username, request_id, artist_name):
  return add_rel_artist_to_playlist(token, username, artist_name, request_id)



class RequestSubmitted1(DomainEvent):
  event_func_name = 'submitted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, artists):
    super().__init__()


class ArtistCreated(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name):
    super().__init__()
