import logging
from atexit import _run_exitfuncs
from itertools import groupby
from operator import itemgetter

import pylast
import spotipy
import spotipy.util as util
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials

from src.apps.music_discovery.signals import artist_url_discovered
from src.apps.read_model.key_value.artist.service import get_unique_artist_id, get_album_info, get_album_tracks, \
  get_track_external_id, \
  get_external_artist_id, get_artist_info, get_unique_track_id, get_track_info
from src.apps.read_model.key_value.genre.service import get_unique_genre_id
from src.domain.artist.commands import CreateArtist, AddAlbum, AddTopTracksToArtist, AddTracksToAlbum, RelateArtist
from src.domain.artist.entities import Artist
from src.domain.artist.errors import DuplicateArtistError, DuplicateAlbumError, InvalidRelatedArtistError
from src.domain.common import constants
from src.domain.genre.commands import CreateGenre
from src.domain.genre.errors import DuplicateGenreError
from src.domain.request.commands import SubmitArtistToRequest
from src.libs.common_domain import aggregate_repository
from src.libs.common_domain.dispatcher import send_command
from src.libs.datetime_utils.datetime_parser import get_datetime
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.scraper_utils.services.dryscrape_scraper import scraper

logger = logging.getLogger(__name__)

client_credentials_manager = SpotifyClientCredentials(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(settings.SPOTIFY_PLAYLIST_USER_NAME, scope, settings.SPOTIFY_CLIENT_ID,
                                   settings.SPOTIFY_CLIENT_SECRET, 'http://localhost/')
user_auth_sp = spotipy.Spotify(auth=token)

network = pylast.LastFMNetwork(settings.LAST_FM_API_KEY, settings.LAST_FM_API_SECRET)


def _relate_artists(root_artist_id, artist_id):
  try:
    ca = RelateArtist(artist_id, constants.SPOTIFY)
    send_command(root_artist_id, ca)
  except InvalidRelatedArtistError:
    pass


def discover_music_for_request(request_id, root_artist_name):
  lfm_artist = _get_lfm_artist_by_name(root_artist_name)

  root_artist = get_sp_artist_by_name(root_artist_name)
  root_artist_id = create_artist_from_spotify_object(root_artist)

  similar_artists = lfm_artist.get_similar(5)
  # similar_artists = lfm_artist.get_similar(25)
  # similar_artists = lfm_artist.get_similar(100)

  similar_artist_names = [a.item.name for a in similar_artists]
  all_artists_names = [lfm_artist.get_name()] + similar_artist_names

  add_artist_to_request_list = []

  for artist_name in all_artists_names:
    try:

      artist = get_sp_artist_by_name(artist_name)
      if not artist: raise IndexError('artist_name: ', artist_name)

      assert artist['name'].lower() == artist_name.lower()

      artist_id = create_artist_from_spotify_object(artist)
      _relate_artists(root_artist_id, artist_id)

      add_artist_to_request_list.append((request_id, artist_id, root_artist_id))

    except (IndexError):
      # this artist isn't in spotify but is in last fm
      pass
    except:
      logger.exception('discover music for %s. similar: %s', root_artist_name, artist_name)

  return add_artist_to_request_list


def _get_lfm_artist_by_name(root_artist_name):
  lfm_artist = network.get_artist(root_artist_name)
  return lfm_artist


def create_album_from_spotify_object(sp_album, artist_id, ):
  release_date = get_datetime(sp_album['release_date'])
  album = _create_album(sp_album['name'], sp_album['popularity'], release_date, constants.SPOTIFY, sp_album['id'],
                        artist_id)

  return album, release_date


def create_album_from_spotify_uri(sp_album_uri, artist_id):
  sp_album = sp.album(sp_album_uri)
  album_id, release_date = create_album_from_spotify_object(sp_album, artist_id, )

  return album_id, release_date


def create_artist_from_spotify_object(artist):
  genres = artist['genres']
  genre_ids = [_create_genre(g, constants.SPOTIFY, g) for g in genres]
  return _create_artist(artist['name'], genre_ids, artist['popularity'], constants.SPOTIFY, artist['id'])


def get_sp_artist_by_name(artist_name):
  sp_artists = sp.search(q='artist:"{0}"'.format(artist_name), type='artist')['artists']['items']
  # todo fuzzy logic? test how many misses we get
  artist = next((sp_artist for sp_artist in sp_artists if sp_artist['name'].lower() == artist_name.lower()), None)
  return artist


def discover_tracks_for_album(album_id, artist_id):
  album_data = get_album_tracks(album_id)
  if not (album_data and album_data.get('tracks')):
    external_id = get_album_info(album_id)['external_id']

    sp_album = sp.album(external_id)
    track_data = _get_tracks_and_audio_info(sp_album['tracks']['items'])

    at = AddTracksToAlbum(album_id, track_data)
    send_command(artist_id, at)


def _get_tracks_and_audio_info(tracks):
  track_ids = [t['id'] for t in tracks]
  sp_tracks = sp.tracks(track_ids)['tracks']
  track_features = sp.audio_features(track_ids)
  track_data = []
  for track_info, track_feature in zip(sp_tracks, track_features):
    track_info_id = track_info['id']
    track_analysis = None
    try:
      track_analysis = sp.audio_analysis(track_info_id)
      track_analysis = {'track': track_analysis['track'], 'sections': track_analysis['sections']}
      track_analysis['track'].pop('codestring', None)
      track_analysis['track'].pop('echoprintstring', None)
      track_analysis['track'].pop('rhythmstring', None)
      track_analysis['track'].pop('synchstring', None)
    except:
      print('track_info_id', track_info_id)

    track_data.append({
      'name': track_info['name'],
      'popularity': track_info['popularity'],
      'features': track_feature,
      'analysis': track_analysis,
      'provider_type': constants.SPOTIFY,
      'external_id': track_info_id,
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

  results = user_auth_sp.user_playlist_replace_tracks(settings.SPOTIFY_PLAYLIST_USER_NAME, playlist_id,
                                                      spotify_track_ids)
  return results


def _create_genre(name, provider_type, external_id):
  genre_id = generate_id()

  try:
    cg = CreateGenre(genre_id, name, provider_type, external_id)
    send_command(genre_id, cg)
  except DuplicateGenreError:
    genre_id = get_unique_genre_id(provider_type, external_id)

  return genre_id


def _create_artist(name, genres, popularity, provider_type, external_id):
  artist_id = generate_id()

  try:
    ca = CreateArtist(artist_id, name, genres, popularity, provider_type, external_id)
    send_command(artist_id, ca)
  except DuplicateArtistError:
    artist_id = get_unique_artist_id(provider_type, external_id)

  return artist_id


def _create_album(name, popularity, release_date, provider_type, external_id, artist_id):
  try:
    album_id = generate_id()
    ca = AddAlbum(album_id, name, popularity, release_date, provider_type, external_id)
    send_command(artist_id, ca)
  except DuplicateAlbumError:
    ag = aggregate_repository.get(Artist, artist_id)
    album_id = ag._get_album_by_external_id(external_id).id

  assert album_id
  return album_id


def submit_artist_to_request(request_id, artist_id, root_artist_id, ):
  add_artist = SubmitArtistToRequest(artist_id, root_artist_id, )
  send_command(request_id, add_artist)
  return artist_id


def discover_top_tracks_for_artist(artist_id):
  external_id = get_external_artist_id(artist_id, constants.SPOTIFY)
  tracks = sp.artist_top_tracks(external_id)['tracks']
  return tracks


def add_artist_top_tracks(artist_id, external_track_ids):
  ag = aggregate_repository.get(Artist, artist_id)
  track_ids = [ag._get_track_by_external_id(t).id for t in external_track_ids]
  at = AddTopTracksToArtist(track_ids)
  send_command(artist_id, at)


_album_properties = ('name', 'popularity', 'release_date')
_feature_properties = (
  'danceability', 'energy', 'loudness', 'speechiness',
  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
)


def _get_flat_track_data_obj(track_info):
  ret_val = {'id': track_info['id'], 'name': track_info['name'], 'popularity': track_info['popularity']}

  features = track_info['features']
  track_features = {k: v for k, v in features.items() if k in _feature_properties}

  ret_val.update(track_features)

  return ret_val


def get_artist_top_track_albums_data(artist_external_id):
  ret_val = []

  internal_artist_id = get_unique_artist_id(constants.SPOTIFY, artist_external_id)
  if internal_artist_id:
    artist_info = get_artist_info(internal_artist_id)
    top_tracks = artist_info['top_tracks']
    top_tracks = sorted(top_tracks, key=_get_album_id_from_track_obj)
    top_tracks = [(k, list(v)) for k, v in groupby(top_tracks, key=_get_album_id_from_track_obj)]
    top_track_albums_dict = dict(top_tracks)

    album_data = [get_album_info(a[0]) for a in top_tracks]
    album_data = list(sorted(album_data, key=itemgetter('release_date')))
    for album in album_data:
      album_info = {k: v for k, v in album.items() if k in _album_properties}
      album_info = {'album': album_info}
      album_info['tracks'] = []
      ret_val.append(album_info)
      album_tracks = get_album_tracks(album['id'])
      tracks = top_track_albums_dict[album['id']]
      for t in tracks:
        track_info = next(tid for tid in album_tracks['tracks'] if tid['id'] == t['track_id'])
        track_data = _get_flat_track_data_obj(track_info)
        album_info['tracks'].append(track_data)
  else:
    pass

  return ret_val


def get_flat_track_data_by_external(track_external_id):
  ret_val = None

  internal_track_id = get_unique_track_id(constants.SPOTIFY, track_external_id)
  if internal_track_id:
    track_info = get_track_info(internal_track_id)
    ret_val = _get_flat_track_data_obj(track_info)
  else:
    pass

  return ret_val


def get_flat_track_data_by_internal(track_id):
  ret_val = None

  track_info = get_track_info(track_id)
  if track_info:
    ret_val = _get_flat_track_data_obj(track_info)

  return ret_val


def _get_album_id_from_track_obj(track):
  return track['album']['id']


def _get_artist_id_from_track_obj(track):
  return track['artists'][0]['id']


def discover_music_from_playlist(attrs, provider_type):
  ret_val = None

  if provider_type == constants.SPOTIFY:
    username = attrs[constants.USER_EXTERNAL_ID]
    playlist_id = attrs[constants.PLAYLIST_EXTERNAL_ID]
    playlist_tracks = [i['track'] for i in sp.user_playlist(username, playlist_id)['tracks']['items']]

    gar = _get_artist_id_from_track_obj
    gal = _get_album_id_from_track_obj
    tracks_grouped_by_artist = sorted(playlist_tracks, key=gar)
    tracks_grouped_by_artist = [(k, list(v)) for k, v in groupby(tracks_grouped_by_artist, key=gar)]

    for artist_key, artist_tracks in tracks_grouped_by_artist:
      # create the unique artist in this list of tracks
      artist_id = artist_tracks[0]['artists'][0]['id']
      artist_obj = sp.artist(artist_id)
      artist_id = create_artist_from_spotify_object(artist_obj)

      tracks_grouped_by_album = sorted(artist_tracks, key=gal)
      tracks_grouped_by_album = [(k, list(v)) for k, v in groupby(tracks_grouped_by_album, key=gal)]

      for album_key, tracks_in_album in tracks_grouped_by_album:
        album_obj = sp.album(album_key)
        create_album_from_spotify_object(album_obj, artist_id)

  return ret_val


def discover_music_from_website(attrs, provider_type):
  ret_val = None

  if provider_type == 'mile-of-music':
    url = attrs[constants.URL]

    # set up a web scraping session
    sess = scraper.Session()

    # we don't need images
    sess.set_attribute('auto_load_images', False)

    # visit homepage and search for a term
    sess.visit(url)
    links = sess.css('#outer-page-wrapper .save-content a')#[:10]
    for link in links:
      artist_url = link.get_attr('href')
      artist_url_discovered.send(None, url=artist_url)

  return ret_val


def discover_music_from_artist_website(url):
  # set up a web scraping session
  sess = scraper.Session()

  # we don't need images
  sess.set_attribute('auto_load_images', False)

  # visit homepage and search for a term
  sess.visit(url)

  spotify_link = sess.at_xpath("//a[contains(@href,'spotify.com/artist')]")
  if spotify_link:
    spotify_id = spotify_link.get_attr('href').split('/')[-1]
    artist = sp.artist(spotify_id)
    artist_id = create_artist_from_spotify_object(artist)


  _run_exitfuncs()
  # guarantees a cleanup
  # https://dryscrape.readthedocs.io/en/latest/apidoc.html#webkit_server.Server.kill
  # https://github.com/closeio/tasktiger/issues/65
