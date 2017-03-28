from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class ArtistCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, provider_type, external_id):
    super().__init__()


class AlbumAdded1(DomainEvent):
  event_func_name = 'album_added_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, release_date, provider_type, external_id, artist_id):
    super().__init__()
