from src.domain.artist.events import ArtistCreated1, AlbumAdded
from src.libs.common_domain.aggregate_base import AggregateBase


class Artist(AggregateBase):
  def __init__(self):
    super().__init__()
    self.albums = []

  @classmethod
  def from_attrs(cls, **kwargs):
    ret_val = cls()

    if not kwargs.get('id'):
      raise TypeError("id is required")

    if not kwargs.get('name'):
      raise TypeError("name is required")

    ret_val._raise_event(ArtistCreated1(**kwargs))

    return ret_val

  def add_album(self, **kwargs):
    self._raise_event(AlbumAdded(**kwargs))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name

  def _handle_album_added_1_event(self, event):
    self.albums.append(event.id)

  def __str__(self):
    return 'Artist {id}: {name}'.format(id=self.id, name=self.name)


class Album:
  def __init__(self, id, name, artist_id):
    if not id:
      raise TypeError("id is required")

    if name is None:
      raise TypeError("name is required")

    if artist_id is None:
      raise TypeError("artist_id is required")

    self.id = id
    self.name = name

    self.artist_id = artist_id

  def __str__(self):
    return 'Album {id}: {name}'.format(id=self.id, score=self.name)


class Track:
  def __init__(self, id, name, album_id):
    if not id:
      raise TypeError("id is required")

    if name is None:
      raise TypeError("name is required")

    if album_id is None:
      raise TypeError("album_id is required")

    self.id = id
    self.name = name

    self.album_id = album_id

  def __str__(self):
    return 'Track {id}: {name}'.format(id=self.id, score=self.name)
