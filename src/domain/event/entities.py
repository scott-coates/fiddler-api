from src.domain.event.events import EventCreated1, ArtistAssociated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Event(AggregateBase):
  def __init__(self):
    super().__init__()
    self._artist_ids = []

  @classmethod
  def from_attrs(cls, id, name, attrs):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not attrs:
      raise TypeError("attrs is required")

    ret_val._raise_event(EventCreated1(id, name, attrs))

    return ret_val

  def associate_artist(self, artist_id):
    assert artist_id

    if artist_id in self._artist_ids:
      raise Exception(f'artist {artist_id} already associated')

    self._raise_event(ArtistAssociated1(artist_id))

  def refresh_playlist(self):
    pass

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.attrs = event.attrs

  def _handle_artist_associated_1_event(self, event):
    self._artist_ids.append(event.artist_id)

  def __str__(self):
    return 'Event {id}: {name}'.format(id=self.id, name=self.name)
