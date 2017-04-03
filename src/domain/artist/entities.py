from itertools import chain

from src.domain.artist.errors import DuplicateAlbumError, DuplicateTrackError, TopTracksExistError
from src.domain.artist.events import ArtistCreated1, AlbumAddedToArtist1, TrackAddedToAlbum1, TopTracksRefreshed1
from src.libs.common_domain.aggregate_base import AggregateBase


class Artist(AggregateBase):
  def __init__(self):
    super().__init__()
    self._albums = []
    self._top_tracks = []

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
    external_id = kwargs['external_id']

    try:
      # check if album already exists
      self._get_album_by_external_id(external_id)
    except:
      self._raise_event(AlbumAddedToArtist1(**kwargs))
    else:
      raise DuplicateAlbumError()

  def add_track(self, **kwargs):
    external_id = kwargs['external_id']

    try:
      # check if track already exists
      self._get_track_by_external_id(external_id)
    except:
      self._get_album_by_id(kwargs['album_id'])
      self._raise_event(TrackAddedToAlbum1(**kwargs))
    else:
      raise DuplicateTrackError()

  def add_top_tracks(self, track_ids):
    if self._top_tracks: raise TopTracksExistError('top tracks already provided.')

    track_data = []
    for t in track_ids:
      # ensure track exists
      track = self._get_track_by_id(t)
      track_data.append({'track_id': t, 'album_id': track.album_id})

    self._raise_event(TopTracksRefreshed1(track_data))

  def _get_album_by_id(self, album_id):
    album = next(album for album in self._albums if album.id == album_id)

    return album

  def _get_album_by_external_id(self, external_id):
    album = next(album for album in self._albums if album.external_id == external_id)

    return album

  def _get_track_by_id(self, track_id):
    albums = self._albums
    tracks = chain.from_iterable(p._tracks for p in albums)
    track = next(track for track in tracks if track.id == track_id)

    return track

  def _get_track_by_external_id(self, external_id):
    albums = self._albums
    tracks = chain.from_iterable(p._tracks for p in albums)
    track = next(track for track in tracks if track.external_id == external_id)

    return track

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.popularity = event.popularity
    self.genres = event.genres

  def _handle_album_added_1_event(self, event):
    self._albums.append(Album(event.id, event.name, event.external_id, self.id))

  def _handle_track_added_1_event(self, event):
    album = self._get_album_by_id(event.album_id)
    album.add_track(event.id, event.name, event.external_id)

  def _handle_top_tracks_refreshed_1_event(self, event):
    self._top_tracks = event.track_ids

  def __str__(self):
    return 'Artist {id}: {name}'.format(id=self.id, name=self.name)


class Album:
  def __init__(self, id, name, external_id, artist_id):
    if not id:
      raise TypeError("id is required")

    if name is None:
      raise TypeError("name is required")

    if artist_id is None:
      raise TypeError("artist_id is required")

    self.id = id
    self.name = name
    self.external_id = external_id

    self._tracks = []

    self.artist_id = artist_id

  def add_track(self, id, name, external_id):
    self._tracks.append(Track(id, name, external_id, self.id))

  def __str__(self):
    return 'Album {id}: {name}'.format(id=self.id, name=self.name)


class Track:
  def __init__(self, id, name, external_id, album_id):
    if not id:
      raise TypeError("id is required")

    if name is None:
      raise TypeError("name is required")

    if album_id is None:
      raise TypeError("album_id is required")

    self.id = id
    self.name = name
    self.external_id = external_id

    self.album_id = album_id

  def __str__(self):
    return 'Track {id}: {name}'.format(id=self.id, score=self.name)
