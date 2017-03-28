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


def discover_music_for_request(request_id, root_artist_name):
  lfm_artist = network.get_artist(root_artist_name)

  similar_artists = lfm_artist.get_similar(2)

  similar_artist_names = [a.item.name for a in similar_artists]
  all_artists_names = [lfm_artist.get_name()] + similar_artist_names

  for artist_name in all_artists_names:
    try:

      artist = sp.search(q='artist:"{0}"'.format(artist_name), type='artist')['artists']['items'][0]
      artist_id = _create_or_get_artist(artist['name'], constants.SPOTIFY, artist['id'])

      albums = sp.search(q='artist:"{0}"'.format(artist_name), limit=50, type='album')['albums']['items']


      for album in albums:
        album_uri = album['uri']

        spotify_album = sp.album(album_uri)
        # release_date = get_datetime(spotify_album['release_date'])
        # if acceptable_age_threshold <= release_date:
        #   last_fm_counter += 1
        #   data.append((artist_name.item.name,
        #                html.escape(artist_name.item.get_bio_summary()).replace('\n', '').replace('|', ''),
        #                spotify_album['name'],
        #                release_date.strftime(
        #                    "%Y-%m-%d")))
        #   # todo don't call this func, use a signal - something like track_discovered.send
        #   add_to_pl(token, username, spotify_album, pl['id'])
    except IndexError:
      pass
    except:
      logger.exception('discover music for %s. similar: %s', artist_name, artist_name)


def _create_or_get_artist(name, provider_type, external_id):
  artist_id = generate_id()

  try:
    ca = CreateArtist(artist_id, name, provider_type, external_id)
    send_command(artist_id, ca)
  except DuplicateArtistError:
    artist_id = get_unique_artist_id(provider_type, external_id)

  return artist_id
