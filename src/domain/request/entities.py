from collections import defaultdict
from operator import itemgetter

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from numpy.random import choice
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

    root_artists = []
    for root_artists_id in self.root_artists_ids:
      root_artists.append(get_artist_info(root_artists_id))

    promoted_artist_calc_data = []
    promoted_artists_data = []
    # go through each promoted artist.
    for artist_id in self._promoted_artist_ids:
      artist_data = get_artist_info(artist_id)
      promoted_artists_data.append(artist_data)

    for promoted_artist in promoted_artists_data:
      genres = set(promoted_artist['genres'])
      highest_genre_overlap = max(len(genres.intersection(set(ra['genres']))) for ra in root_artists)
      promoted_artist_calc_data.append({'id': promoted_artist['id'], 'genre_score': highest_genre_overlap})

    # does this promoted artist match enough genres of any root artists
    for a in sorted(promoted_artist_calc_data, key=itemgetter('genre_score'), reverse=True):
      artist_data = get_artist_info(a['id'])

      # Get it's most popular tracks. are they recent? are they in the promoted albums?
      for top_track in artist_data['top_tracks']:
        top_track_album_id = top_track['album_id']
        if top_track_album_id in self._promoted_album_ids:
          playlist_track_ids.append(top_track['track_id'])

    if playlist_track_ids:
      # track_count = choice([10,11,12,13,14,15,16], p=[0.75, 0.2, 0.05])
      track_count = random.choice(range(10, 16))
      playlist_track_ids = [playlist_track_ids[i] for i in
                            sorted(random.sample(range(len(playlist_track_ids)), track_count))]

    self._raise_event(
        PlaylistRefreshedWithTracks1(playlist_track_ids, self.playlist.provider_type, self.playlist.external_id))

    # if so, does this song seem similar enough to the top track of any root artists?
    # does this anchor song have a good follow up song? a smooth transition song?
    # go through each root artist


    #
    # # get root artist info
    #
    # # root_artist_top_tracks = self.root_artists_ids =
    #
    # # artist data
    # # what else - i'll need artist info
    # # i'll need track info
    # current_tracks = self.playlist.track_ids
    #
    # track_ids = [t['id'] for t in album['tracks']]
    #
    # probability = [t['features']['energy'] if t['features'] else .5 for t in album['tracks']]
    # sum_probability = sum(probability)
    # probability = [p / sum_probability for p in probability]
    #
    # track_count = choice([0, 1, 2], p=[0.75, 0.2, 0.05])
    #
    # # todo use python 3.6 built-in choices func
    # track_ids = list(set(choice(track_ids, track_count, p=probability)))
    #
    # if track_ids:
    #   track_ids.extend(self.playlist.track_ids)
    #   assert len(set(track_ids)) == len(track_ids), 'track_ids exist already: %s' % track_ids
    #   self._raise_event(
    #       PlaylistRefreshedWithTracks1(track_ids, self.playlist.provider_type, self.playlist.external_id, album_id))

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
