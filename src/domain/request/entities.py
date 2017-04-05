from collections import defaultdict
from itertools import groupby
from operator import itemgetter

from dateutil.relativedelta import relativedelta
from django.utils import timezone

import random

from src.apps.music_discovery.service import create_playlist
from src.apps.read_model.key_value.artist.service import get_artist_info, get_artist_albums, get_album_tracks, \
  get_album_info
from src.domain.common import constants
from src.domain.request.errors import DuplicateAlbumInRequestError, InvalidRequestError
from src.domain.request.events import RequestSubmitted1, PlaylistCreatedForRequest, \
  PlaylistRefreshedWithTracks1, ArtistPromotedToRequest1, ArtistSkippedByRequest1
from src.domain.request.value_objects import SpotifyPlaylist
from src.libs.common_domain.aggregate_base import AggregateBase

acceptable_age_threshold = timezone.now() - relativedelta(months=18)


def _get_track_count_per_root_artist(root_artist_count):
  track_count = random.choice(range(10, 16))
  ret_val = max(round(track_count / root_artist_count), 1)
  return ret_val


def _get_album_id(a):
  return a['album_id']


class Request(AggregateBase):
  def __init__(self):
    super().__init__()
    self._promoted_artists = defaultdict(list)
    self._skipped_artists = defaultdict(list)
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
    external_url = playlist['external_urls']['spotify']
    ret_val._raise_event(PlaylistCreatedForRequest(playlist['name'], constants.SPOTIFY, playlist['id'], external_url))

    return ret_val

  def submit_potential_artist(self, artist_id, root_artist_id):
    assert artist_id
    assert root_artist_id

    # it's possible other request artists triggered this album to be processed already.
    if artist_id not in self._promoted_artists[root_artist_id]:

      artist_albums = get_artist_albums(artist_id)

      album_data = [get_album_info(a) for a in artist_albums]
      most_recent_album = max(a['release_date'] for a in album_data)

      if acceptable_age_threshold <= most_recent_album:
        self._raise_event(ArtistPromotedToRequest1(artist_id, root_artist_id))
      else:
        self._raise_event(ArtistSkippedByRequest1(artist_id, root_artist_id))

  def refresh_playlist(self):
    if self.playlist.track_ids: raise InvalidRequestError('playlist already refreshed')

    playlist_track_ids = []

    root_artist_count = len(self._promoted_artists)

    track_count_per_root_artist = _get_track_count_per_root_artist(root_artist_count)

    for root_artist_id, promoted_artist_ids in self._promoted_artists.items():
      counter = 0
      root_artists = []
      promoted_artists_data = []

      root_artist_data = get_artist_info(root_artist_id)
      root_artist_genres = root_artist_data['genres']

      for promoted_artist_id in promoted_artist_ids:
        promoted_artist_data = get_artist_info(promoted_artist_id)
        promoted_artists_data.append(promoted_artist_data)

      sorted_promoted_artists = sorted(promoted_artists_data,
                                       key=lambda a: root_artist_genres.intersection(a['genres']), reverse=True)
      for pa in sorted_promoted_artists:
        # get top tracks from artist
        top_track_albums = defaultdict(list)

        pa_top_tracks = sorted(pa['top_tracks'], key=_get_album_id)
        for track in pa_top_tracks:
          top_track_albums[track['album_id']].append(track['track_id'])

        # grouped_top_tracks_by_album = groupby(pa_top_tracks, _get_album_id) -- NOT WORKING
        albums = {a: get_album_info(a) for a in top_track_albums.keys()}
        for album_id, top_track_ids in top_track_albums.items():
          album = albums[album_id]
          if acceptable_age_threshold <= album['release_date']:
            for track_id in top_track_ids:
              if counter <= track_count_per_root_artist:
                if random.choices([0, 1], weights=[0.8, 0.2])[0]:
                  playlist_track_ids.append(track_id)
                  counter += 1
              else:
                # we've reached the breaking point, no more tracks for this root artist
                break
            else:
              # http://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
              # break out of nested loops
              continue
            break
        else:
          continue
        break

    if playlist_track_ids:
      self._raise_event(
          PlaylistRefreshedWithTracks1(playlist_track_ids, self.playlist.provider_type, self.playlist.external_id))

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.root_artists_ids = event.data['artist_ids']

  def _handle_artist_promoted_1_event(self, event):
    self._promoted_artists[event.data['root_artist_id']].append(event.data['artist_id'])

  def _handle_artist_skipped_1_event(self, event):
    pass

  def _handle_playlist_created_1_event(self, event):
    self.playlist = SpotifyPlaylist(event.data['provider_type'], event.data['external_id'])

  def _handle_playlist_refreshed_1_event(self, event):
    self.playlist = SpotifyPlaylist(self.playlist.provider_type, self.playlist.external_id, event.data['track_ids'])

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
