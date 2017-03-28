import logging

import pylast
import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyClientCredentials

from src.apps.read_model.key_value.artist.service import get_unique_artist_id
from src.domain.artist.commands import CreateArtist
from src.domain.artist.errors import DuplicateArtistError
from src.domain.common import constants
from src.libs.common_domain.dispatcher import send_command
from src.libs.python_utils.id.id_utils import generate_id

logger = logging.getLogger(__name__)

client_credentials_manager = SpotifyClientCredentials(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

network = pylast.LastFMNetwork(settings.LAST_FM_API_KEY, settings.LAST_FM_API_SECRET)


def discover_music_for_request(request_id, artist_name):
  artist = network.get_artist(artist_name)

  result = sp.search(q='artist:"{0}"'.format(artist.name), type='artist')

  sp_artist = result['artists']['items'][0]
  artist_id = _create_or_get_artist(sp_artist['name'], constants.SPOTIFY, sp_artist['id'])

  similar_artists = artist.get_similar(2)
  return
  for similar_artist in similar_artists:
    try:
      albums = sp.search(q='artist:' + similar_artist.item.name, limit=50, type='album')['albums']['items']

      for album in albums:
        album_uri = album['uri']

        spotify_album = sp.album(album_uri)
        # release_date = get_datetime(spotify_album['release_date'])
        # if acceptable_age_threshold <= release_date:
        #   last_fm_counter += 1
        #   data.append((similar_artist.item.name,
        #                html.escape(similar_artist.item.get_bio_summary()).replace('\n', '').replace('|', ''),
        #                spotify_album['name'],
        #                release_date.strftime(
        #                    "%Y-%m-%d")))
        #   # todo don't call this func, use a signal - something like track_discovered.send
        #   add_to_pl(token, username, spotify_album, pl['id'])
    except:
      logger.exception('discover music for', artist, ': similar', similar_artist)


def _create_or_get_artist(name, provider_type, external_id):
  artist_id = generate_id()

  try:
    ca = CreateArtist(artist_id, name, provider_type, external_id)
    send_command(artist_id, ca)
  except DuplicateArtistError:
    artist_id = get_unique_artist_id(provider_type, external_id)

  return artist_id
