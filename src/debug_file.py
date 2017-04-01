import django

from src.domain.request.commands import SubmitRequest
from src.libs.common_domain.dispatcher import send_command

django.setup()

# region bootstrap interact
from src.libs.python_utils.id.id_utils import generate_id

request_id = generate_id()



artists = """
tycho
"""

# artists = """
# Against Me!
# Pussy Riot
# Saul Williams
# """

artists = list(filter(bool, artists.split('\n')))

send_command(-1, SubmitRequest(request_id, artists))

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
