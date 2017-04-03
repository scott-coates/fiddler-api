from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class ArtistCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, genres, popularity, provider_type, external_id):
    super().__init__()


class AlbumAddedToArtist1(DomainEvent):
  event_func_name = 'album_added_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, release_date, provider_type, external_id):
    super().__init__()


class TrackAddedToAlbum1(DomainEvent):
  event_func_name = 'track_added_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, popularity, features, provider_type, external_id, album_id):
    super().__init__()


class TopTracksRefreshed1(DomainEvent):
  event_func_name = 'top_tracks_refreshed_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, track_ids, ):
    super().__init__()
