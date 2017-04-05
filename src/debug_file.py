import django

django.setup()
from src.apps.read_model.key_value.artist.service import get_album_tracks
from src.domain.request.entities import Request
from src.libs.common_domain import aggregate_repository, event_repository

from src.apps.music_discovery.service import get_sp_artist_by_name, create_artist_from_spotify_object
from src.domain.request.commands import SubmitRequest
from src.libs.common_domain.dispatcher import send_command

from src.libs.python_utils.id.id_utils import generate_id

# region bootstrap interact

request_id = generate_id()
import logging

logger = logging.getLogger(__name__)


artists = """
tycho
ratatat
"""

# artists = """
# Against Me!
# Pussy Riot
# Saul Williams
# """

artists = list(filter(bool, artists.split('\n')))

artists_info = ([], [])
for artist_name in artists:
  artist = get_sp_artist_by_name(artist_name)
  artist_id = create_artist_from_spotify_object(artist)
  artists_info[0].append(artist_id)
  artists_info[1].append(artist['name'])
send_command(-1, SubmitRequest(request_id, artists_info[0], artists_info[1]))

# endregion

# region vanilla
# import spotipy
# import spotipy.util as util
#
# scope = 'playlist-modify-public'
# token = util.prompt_for_user_token('punkrockplaylist', scope, settings.SPOTIFY_CLIENT_ID,
#                                    settings.SPOTIFY_CLIENT_SECRET, 'http://localhost/')
#
# create_playlist.delay(token, 'punkrockplaylist', request_id)
#
# for artist in artists:
#   populate_request.delay(token, 'punkrockplaylist', request_id, artist)

# endregion

# region playlist curation
# request_id = generate_id()
#
# ag = aggregate_repository.get(Request, "oH6suwyH")
#
# # events = event_repository.get_events(['ArtistPromotedToRequest1']).filter(stream_id=ag.id)
# #
# # for event in events:
# #   album = get_album_data(event.event_data['album_id'])
#
# version  = ag.version
# ag.refresh_playlist()
#
# aggregate_repository.save(ag, version)
# endregion
