from dateutil.relativedelta import relativedelta
from django.utils import timezone
from numpy.random import choice

from src.apps.music_discovery.service import create_playlist
from src.domain.common import constants
from src.domain.request.errors import DuplicateAlbumInRequestError, InvalidAlbumRequestError
from src.domain.request.events import RequestSubmitted1, PlaylistCreatedForRequest, \
  PlaylistRefreshedWithTracks1, AlbumPromotedToRequest1
from src.domain.request.value_objects import SpotifyPlaylist
from src.libs.common_domain.aggregate_base import AggregateBase

acceptable_age_threshold = timezone.now() - relativedelta(months=18)


class Request(AggregateBase):
  def __init__(self):
    super().__init__()
    self._promoted_albums = []
    self._playlist_albums = []
    self.playlist = None

  @classmethod
  def submit(cls, id, artist_ids, artist_names):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artist_ids or not all(artist_ids):
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artist_ids, artist_names))

    # todo have this be in its own event handler
    playlist = create_playlist(id)
    ret_val._raise_event(PlaylistCreatedForRequest(playlist['name'], constants.SPOTIFY, playlist['id']))

    return ret_val

  def submit_potential_album(self, album_id, release_date, artist_id):
    assert album_id
    assert release_date
    assert artist_id

    if album_id not in self._promoted_albums:
      # it's possible other request artists triggered this album to be processed already.
      if acceptable_age_threshold <= release_date:
        self._raise_event(AlbumPromotedToRequest1(album_id, artist_id))

        #todo refresh w/ artist
  def refresh_playlist_with_album(self, album):
    album_id = album['id']

    if album_id not in self._promoted_albums: raise InvalidAlbumRequestError('album no promoted:', album_id)
    if album_id in self._playlist_albums: raise DuplicateAlbumInRequestError('album already in playlist:', album_id)

    # go through each artist
      # get root artist info

    # root_artist_top_tracks = self.root_artists_ids =

    # artist data
    # what else - i'll need artist info
    # i'll need track info
    current_tracks = self.playlist.track_ids

    track_ids = [t['id'] for t in album['tracks']]

    probability = [t['features']['energy'] if t['features'] else .5 for t in album['tracks']]
    sum_probability = sum(probability)
    probability = [p / sum_probability for p in probability]

    track_count = choice([0, 1, 2], p=[0.75, 0.2, 0.05])

    # todo use python 3.6 built-in choices func
    track_ids = list(set(choice(track_ids, track_count, p=probability)))

    if track_ids:
      track_ids.extend(self.playlist.track_ids)
      assert len(set(track_ids)) == len(track_ids), 'track_ids exist already: %s' % track_ids
      self._raise_event(
          PlaylistRefreshedWithTracks1(track_ids, self.playlist.provider_type, self.playlist.external_id, album_id))

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.root_artists_ids = event.data['artist_ids']

  def _handle_album_promoted_1_event(self, event):
    self._promoted_albums.append(event.album_id)

  def _handle_playlist_created_1_event(self, event):
    self.playlist = SpotifyPlaylist(event.data['provider_type'], event.data['external_id'])

  def _handle_playlist_refreshed_1_event(self, event):
    self.playlist = SpotifyPlaylist(self.playlist.provider_type, self.playlist.external_id, event.data['track_ids'])
    self._playlist_albums.append(event.data['album_id'])

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
