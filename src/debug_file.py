import django

django.setup()

# region bootstrap interact
from src.libs.python_utils.id.id_utils import generate_id

request_id = generate_id()



artists = """
make war
"""

artists = list(filter(bool, artists.split('\n')))

# send_command(-1, SubmitRequest(request_id, artists))

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
