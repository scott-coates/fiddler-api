from django_rq import job

from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer
from src.music import get_new_rel_artists


@job('high')
def populate_request(request_id, artist):
  return get_new_rel_artists(artist)


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
