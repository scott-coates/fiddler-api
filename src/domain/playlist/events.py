from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class PlaylistCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, entity_type, entity_id):
    super().__init__()


class ExternalPlaylistGenerated1(DomainEvent):
  event_func_name = 'external_playlist_generated_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, name, provider_type, external_id, external_url):
    super().__init__()
