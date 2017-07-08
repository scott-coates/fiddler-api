import random

from src.apps.music_discovery.service import create_playlist
from src.apps.read_model.key_value.artist.service import get_artist_info
from src.domain.common import constants
from src.domain.common.value_objects.playlist import Playlist
from src.domain.event.events import EventCreated1, ArtistAssociated1, EventPlaylistRefreshedWithTracks1, \
  PlaylistCreatedForEvent
from src.domain.request.events import PlaylistCreatedForRequest
from src.libs.common_domain.aggregate_base import AggregateBase


class Event(AggregateBase):
  def __init__(self):
    super().__init__()
    self._artist_ids = []
    self.playlist = None

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

  def create_playlist(self):
    if self.playlist:
      raise Exception('playlist already created')

    playlist = create_playlist(self.id)
    external_url = playlist['external_urls']['spotify']
    self._raise_event(PlaylistCreatedForEvent(playlist['name'], constants.SPOTIFY, playlist['id'], external_url))

  def refresh_playlist(self):
    if self.playlist and self.playlist.track_ids: raise Exception('playlist already refreshed')

    playlist_track_ids = []
    # loop through each artist
    # add top three tracks to playlist

    for artist_id in self._artist_ids:
      artist_info = get_artist_info(artist_id)
      top_tracks = artist_info['top_tracks']

      chosen_tracks = random.sample(top_tracks, k=3)

      playlist_track_ids.extend(t['track_id'] for t in chosen_tracks)

    self._raise_event(
      EventPlaylistRefreshedWithTracks1(playlist_track_ids, self.playlist.provider_type, self.playlist.external_id)
    )

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.attrs = event.attrs

  def _handle_artist_associated_1_event(self, event):
    self._artist_ids.append(event.artist_id)

  def _handle_playlist_created_1_event(self, event):
    self.playlist = Playlist(event.data['provider_type'], event.data['external_id'])

  def _handle_playlist_refreshed_1_event(self, event):
    self.playlist = Playlist(event.data['provider_type'], event.data['external_id'])

  def __str__(self):
    return 'Event {id}: {name}'.format(id=self.id, name=self.name)
