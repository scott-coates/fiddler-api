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


class EventPlaylistRefreshedWithTracks1(DomainEvent):
  event_func_name = 'playlist_refreshed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, track_ids, provider_type, external_id):
    super().__init__()


class PlaylistCreatedForEvent(DomainEvent):
  event_func_name = 'playlist_created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, name, provider_type, external_id, external_url):
    super().__init__()

