import html

import pylast
import spotipy
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone

from src.libs.datetime_utils.datetime_parser import get_datetime

acceptable_age_threshold = timezone.now() - relativedelta(months=18)

sp = spotipy.Spotify()

network = pylast.LastFMNetwork(settings.LAST_FM_API_KEY, settings.LAST_FM_API_SECRET)

def get_new_rel_artists(artist_name):
  data = []

  artist = network.get_artist(artist_name)
  similar = artist.get_similar(5)
# similar = artist.get_similar(40)
  similar_count = len(similar)
  real_name = artist.name
  total_count = 0
  print('Last FM Related artists for', real_name)
  for i, sim in enumerate(similar, 1):
    try:
      last_fm_counter = 0
      albums = sim.item.get_top_albums()
      results = sp.search(q='artist:' + sim.item.name, type='album')['albums']
      sp_artist_albums = results['items']

      for album in albums:
        try:
          album_name = album.item.get_name().lower()
          spotify_album_result = next(x for x in sp_artist_albums if x['name'].lower() == album_name)
        except:
          pass
        else:
          album_uri = spotify_album_result['uri']
          spotify_album = sp.album(album_uri)
          release_date = get_datetime(spotify_album['release_date'])
          if acceptable_age_threshold <= release_date:
            last_fm_counter += 1
            data.append((sim.item.name, html.escape(sim.item.get_bio_summary()).replace('\n', '').replace('|', ''),
                         spotify_album['name'],
                         release_date.strftime(
                             "%Y-%m-%d")))


      total_count += last_fm_counter
      print('  ', i, 'of', similar_count, sim.item.name, '\t\t\t\t\t\t  Found', last_fm_counter)
    except:
      print('error retrieving', sim.item.name)



  def _get_extracted_from_result_set(result_set):
    result_set = sorted([s.item.name for s in result_set])
    result_text = ', '.join(result_set)
    return result_text
