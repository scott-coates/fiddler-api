import django

from src.domain.common import constants
from src.domain.event.commands import CreateEvent
from src.domain.source.commands import CreateSource

django.setup()
from src.apps.read_model.key_value.artist.service import get_album_tracks
from src.domain.request.entities import Request
from src.libs.common_domain import aggregate_repository, event_repository

from src.apps.music_discovery.service import get_sp_artist_by_name, create_artist_from_spotify_object
from src.domain.request.commands import SubmitRequest
from src.libs.common_domain.dispatcher import send_command
from src.libs.python_utils.id.id_utils import generate_id

import logging
import sys

logger = logging.getLogger(__name__)

# region bootstrap interact
# from django.core.management import call_command
source_id = generate_id()
request_id = generate_id()
#
# call_command('clear_log_files')
#
# source_attrs = {constants.USER_EXTERNAL_ID: 'spotify', constants.PLAYLIST_EXTERNAL_ID: '37i9dQZF1DX0KpeLFwA3tO'}
# send_command(-1, CreateSource(
#     source_id, 'Spotify New Punk Tracks Playlist',
#     constants.SPOTIFY, constants.PLAYLIST,
#     source_attrs
# ))

# source_attrs = {constants.USER_EXTERNAL_ID: 'spotify', constants.PLAYLIST_EXTERNAL_ID: '37i9dQZF1DX0KpeLFwA3tO'}
# source_attrs = {constants.URL: 'https://mileofmusic.com/lineup/'}
#
# send_command(-1, CreateSource(
#     source_id, 'MoM 2017',
#     'mile-of-music', constants.WEBSITE,
#     source_attrs
# ))
# after a website is scraped, artists are obtained and they're genre's are captured and a schedule to get their top tracks is setup as well
# now i have an event that is created - Event, name, --> attrs like the artist_listing_page
# this event will in turn create a source
# when all bands are scraped from the source, we want to create a playlist for the event
# and a playlist for each 'good' genre - some genres are too niche - selected genres

event_attrs = {constants.URL: 'https://mileofmusic.com/lineup/'}

send_command(-1, CreateEvent(
  source_id, 'MoM 2017',
  event_attrs
))


# artists = """
# hot water music
# """
#
# artists = list(filter(bool, artists.split('\n')))
#
# artists_info = ([], [])
# for artist_name in artists:
#   artist = get_sp_artist_by_name(artist_name)
#   artist_id = create_artist_from_spotify_object(artist)
#   artists_info[0].append(artist_id)
#   artists_info[1].append(artist['name'])
# send_command(-1, SubmitRequest(request_id, artists_info[0], artists_info[1]))

# endregion

# region scraper
# import dryscrape
#
# if 'linux' in sys.platform:
#   # start xvfb in case no X is running. Make sure xvfb
#   # is installed, otherwise this won't work!
#   dryscrape.start_xvfb()
#
# search_term = 'dryscrape'
#
# # set up a web scraping session
# sess = dryscrape.Session(base_url='http://google.com')
#
# # we don't need images
# sess.set_attribute('auto_load_images', False)
#
# # visit homepage and search for a term
# sess.visit('/')
# q = sess.at_xpath('//*[@name="q"]')
# q.set(search_term)
# q.form().submit()
#
# # extract all links
# for link in sess.xpath('//a[@href]'):
#   print(link['href'])
#
# # save a screenshot of the web page
# sess.render('google.png')
# print("Screenshot written to 'google.png'")
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
