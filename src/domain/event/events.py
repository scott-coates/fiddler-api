from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class EventCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, attrs):
    super().__init__()


class ArtistAssociated1(DomainEvent):
  event_func_name = 'artist_associated_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, artist_id):
    super().__init__()
