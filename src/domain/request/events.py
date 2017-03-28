from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class RequestSubmitted1(DomainEvent):
  event_func_name = 'submitted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, artists):
    super().__init__()


class AlbumAddedToRequest1(DomainEvent):
  event_func_name = 'album_added_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, album_id, artist_id):
    super().__init__()
