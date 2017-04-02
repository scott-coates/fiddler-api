import logging
import random

import pylast
import spotipy
import spotipy.util as util
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials

from src.apps.read_model.key_value.artist.service import get_unique_artist_id, get_album_external_id, get_album_data, \
  get_track_external_id, \
  get_album_id, get_external_artist_id
from src.domain.artist.commands import CreateArtist, CreateAlbum, AddTracks
from src.domain.artist.errors import DuplicateArtistError, DuplicateAlbumError
from src.domain.common import constants
from src.domain.request.commands import AddAlbumToRequest
from src.libs.common_domain.dispatcher import send_command
from src.libs.datetime_utils.datetime_parser import get_datetime
from src.libs.python_utils.id.id_utils import generate_id

logger = logging.getLogger(__name__)

client_credentials_manager = SpotifyClientCredentials(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(settings.SPOTIFY_PLAYLIST_USER_NAME, scope, settings.SPOTIFY_CLIENT_ID,
                                   settings.SPOTIFY_CLIENT_SECRET, 'http://localhost/')
user_auth_sp = spotipy.Spotify(auth=token)

network = pylast.LastFMNetwork(settings.LAST_FM_API_KEY, settings.LAST_FM_API_SECRET)


def discover_music_for_request(request_id, root_artist_name):
  lfm_artist = network.get_artist(root_artist_name)

  similar_artists = lfm_artist.get_similar(2)
  # similar_artists = lfm_artist.get_similar(100)

  similar_artist_names = [a.item.name for a in similar_artists]
  all_artists_names = [lfm_artist.get_name()] + similar_artist_names

  for artist_name in all_artists_names:
    try:

      artist = get_sp_artist_by_name(artist_name)
      if not artist: raise IndexError('artist_name: ', artist_name)

      assert artist['name'].lower() == artist_name.lower()

      artist_id = create_artist_from_spotify_object(artist)

      albums = sp.artist_albums(artist['id'])['items']

      for album in albums:
        album_id = get_album_id(constants.SPOTIFY, album['id'])

        if not album_id:
          album_uri = album['uri']
          sp_album = sp.album(album_uri)
          album_id, release_date = create_album_from_spotify_object(artist_id, sp_album)
        else:
          release_date = get_datetime(get_album_external_id(album_id)['release_date'])

        _add_album_to_request(request_id, album_id, release_date, artist_id)
    except (IndexError):
      # this artist isn't in spotify but is in last fm
      pass
    except:
      logger.exception('discover music for %s. similar: %s', artist_name, artist_name)


def create_album_from_spotify_object(artist_id, sp_album):
  return _create_album(sp_album['name'], get_datetime(sp_album['release_date']), constants.SPOTIFY, sp_album['id'],
                       artist_id)


def create_artist_from_spotify_object(artist):
  return _create_artist(artist['name'], artist['genres'], artist['popularity'], constants.SPOTIFY, artist['id'])


def get_sp_artist_by_name(artist_name):
  sp_artists = sp.search(q='artist:"{0}"'.format(artist_name), type='artist')['artists']['items']
  # todo fuzzy logic? test how many misses we get
  artist = next((sp_artist for sp_artist in sp_artists if sp_artist['name'].lower() == artist_name.lower()), None)
  return artist


def discover_tracks_for_album(album_id, artist_id):
  album_data = get_album_data(album_id)
  if not (album_data and album_data.get('tracks')):
    external_id = get_album_external_id(album_id)['external_id']

    sp_album = sp.album(external_id)
    track_data = _get_tracks_and_features(album_id, sp_album['tracks']['items'])

    at = AddTracks(track_data)
    send_command(artist_id, at)


def _get_tracks_and_features(album_id, tracks):
  track_ids = [t['id'] for t in tracks]
  track_features = sp.audio_features(track_ids)
  track_data = []
  for track_info, track_feature in zip(tracks, track_features):
    track_data.append({
      'name': track_info['name'],
      'features': track_feature,
      'provider_type': constants.SPOTIFY,
      'external_id': track_info['id'],
      'album_id': album_id,
    })
  return track_data


def create_playlist(name):
  playlist = user_auth_sp.user_playlist_create(settings.SPOTIFY_PLAYLIST_USER_NAME, name)
  return playlist


def update_playlist_with_tracks(playlist_id, track_ids, ):
  spotify_track_ids = []

  for t in track_ids:
    track_data = get_track_external_id(t)
    spotify_track_ids.append(track_data['external_id'])
    spotify_track_ids = random.sample(spotify_track_ids, min(100, len(spotify_track_ids)))

  results = user_auth_sp.user_playlist_replace_tracks(settings.SPOTIFY_PLAYLIST_USER_NAME, playlist_id,
                                                      spotify_track_ids)
  return results


def _create_artist(name, genres, popularity, provider_type, external_id):
  artist_id = generate_id()

  try:
    ca = CreateArtist(artist_id, name, genres, popularity, provider_type, external_id)
    send_command(artist_id, ca)
  except DuplicateArtistError:
    artist_id = get_unique_artist_id(provider_type, external_id)

  return artist_id


def _create_album(name, release_date, provider_type, external_id, artist_id):
  try:
    album_id = generate_id()
    ca = CreateAlbum(album_id, name, release_date, provider_type, external_id)
    send_command(artist_id, ca)
  except DuplicateAlbumError:
    album_id = get_album_id(provider_type, external_id)

  return album_id


def _add_album_to_request(request_id, album_id, release_date, artist_id):
  add_album = AddAlbumToRequest(album_id, release_date, artist_id, )
  send_command(request_id, add_album)
  return album_id


def discover_top_tracks_for_artist(artist_id):
  external_id = get_external_artist_id(artist_id, constants.SPOTIFY)
  tracks = sp.artist_top_tracks(external_id)['tracks']
  return tracks
