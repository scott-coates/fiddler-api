from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.apps.music_discovery.service import create_playlist
from src.domain.common import constants
from src.domain.request.events import RequestSubmitted1, AlbumAddedToRequest1, PlaylistCreatedForRequest, \
  PlaylistRefreshedWithTracks1
from src.domain.request.value_objects import SpotifyPlaylist
from src.libs.common_domain.aggregate_base import AggregateBase
from numpy.random import choice
import random

acceptable_age_threshold = timezone.now() - relativedelta(months=18)


class Request(AggregateBase):
  def __init__(self):
    super().__init__()
    self.albums = []
    self.playlist = None

  @classmethod
  def submit(cls, id, artist_names):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artist_names or not all(artist_names):
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artist_names))

    # todo have this be in its own event handler
    playlist = create_playlist(id)
    ret_val._raise_event(PlaylistCreatedForRequest(playlist['name'], constants.SPOTIFY, playlist['id']))

    return ret_val

  def add_album(self, album_id, release_date, artist_id):
    if acceptable_age_threshold <= release_date:
      self._raise_event(AlbumAddedToRequest1(album_id, artist_id))

  def refresh_playlist_with_album(self, album):

    # i'm gonna need album data
    # artist data
    # what else - i'll need artist info
    # i'll need track info
    current_tracks = self.playlist.track_ids

    album_id = album['id']

    track_ids = [t['id'] for t in album['tracks']]
    probability = [t['features']['energy'] for t in album['tracks']]
    sum_probability = sum(probability)
    probability = [p / sum_probability for p in probability]
    track_count = random.randint(0, 2)

    # todo use python 3.6 built-in choices func
    track_ids = list(choice(track_ids, track_count, p=probability))

    track_ids.extend(self.playlist.track_ids)

    self._raise_event(PlaylistRefreshedWithTracks1(self.playlist.provider_type, self.playlist.external_id, track_ids))

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.artists_names = event.data['artist_names']

  def _handle_album_added_1_event(self, event):
    self.albums.append(event.album_id)

  def _handle_playlist_created_1_event(self, event):
    self.playlist = SpotifyPlaylist(event.data['provider_type'], event.data['external_id'])

  def _handle_playlist_refreshed_1_event(self, event):
    self.playlist = SpotifyPlaylist(self.playlist.provider_type, self.playlist.external_id, event.data['track_ids'])

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
