from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.apps.music_discovery.service import create_playlist
from src.domain.common import constants
from src.domain.request.events import RequestSubmitted1, AlbumAddedToRequest1, PlaylistCreatedForRequest, \
  TrackAddedToPlaylist1
from src.domain.request.value_objects import SpotifyPlaylist
from src.libs.common_domain.aggregate_base import AggregateBase

acceptable_age_threshold = timezone.now() - relativedelta(months=500)


class Request(AggregateBase):
  def __init__(self):
    super().__init__()
    self.albums = []
    self.playlist = None

  @classmethod
  def submit(cls, id, artists):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artists or not all(artists):
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artists))

    # todo have this be in its own event handler
    # playlist = create_playlist(id)
    # ret_val._raise_event(PlaylistCreatedForRequest(playlist['name'], constants.SPOTIFY, playlist['id']))

    return ret_val

  def add_album(self, album_id, release_date, artist_id):
    if acceptable_age_threshold <= release_date:
      self._raise_event(AlbumAddedToRequest1(album_id, artist_id))

  def refresh_playlist_with_album(self, album):

    # i'm gonna need album data
    # artist data
    # what else - i'll need artist info
    # i'll need track info
    current_tracks = self.playlist.tracks

    album_id = album['id']

    for track in album['tracks']:
      self._raise_event(TrackAddedToPlaylist1(track['id']))

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.artists = event.artists

  def _handle_album_added_1_event(self, event):
    self.albums.append(event.album_id)

  def _handle_playlist_created_1_event(self, event):
    self.playlist = SpotifyPlaylist(event.data['external_id'])

  def _handle_track_added_1_event(self, event):
    tracks = self.playlist.tracks
    all_tracks = [event.data['track']]

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
