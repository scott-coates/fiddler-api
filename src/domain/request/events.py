from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class RequestSubmitted1(DomainEvent):
  event_func_name = 'submitted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, artist_ids, artist_names):
    super().__init__()


class ArtistPromotedToRequest1(DomainEvent):
  event_func_name = 'artist_promoted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, artist_id, root_artist_id):
    super().__init__()


class ArtistSkippedByRequest1(DomainEvent):
  event_func_name = 'artist_skipped_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, artist_id, root_artist_id):
    super().__init__()


class PlaylistRefreshedWithTracks1(DomainEvent):
  event_func_name = 'playlist_refreshed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, track_ids, artist_ids_in_playlist, provider_type, external_id):
    super().__init__()


class RequestLinkedWithPlaylist1(DomainEvent):
  event_func_name = 'playlist_linked_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, playlist_id):
    super().__init__()
