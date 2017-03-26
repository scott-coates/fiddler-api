import html

import pylast
import spotipy
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from tabulate import tabulate

from src.libs.datetime_utils.datetime_parser import get_datetime

artist_name = 'sum 41'
data = []
acceptable_age_threshold = timezone.now() - relativedelta(months=18)

sp = spotipy.Spotify()
import os

network = pylast.LastFMNetwork(settings.LAST_FM_API_KEY, settings.LAST_FM_API_SECRET)

artist = network.get_artist(artist_name)
similar = artist.get_similar(100)
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
    # paging pattern - https://spotipy.readthedocs.io/en/latest/#welcome-to-spotipy
    # the paging pattern is slow and delivers unnecessary albums (from compilations and wrong artists)...
    # while results['next']:
    #   results = sp.next(results)['albums']
    #   sp_artist_albums.extend(results['items'])

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

print()
print()
result = sp.search(q='artist:' + artist_name, type='artist')

try:
  # raise Exception()
  sp_artist = result['artists']['items'][0]
  name = sp_artist['name']
  uri = sp_artist['uri']

  related = sp.artist_related_artists(uri)
  all_artists = [sp_artist] + related['artists']
  similar_count = len(all_artists)

  print('Spotify Related artists for', name)
  for i, rel_artist in enumerate(all_artists, 1):
    last_fm_artist = network.get_artist(rel_artist['name'])
    sp_counter = 0
    rel_uri = rel_artist['uri']

    results = sp.artist_albums(rel_uri)
    albums = results['items']

    # paging pattern - https://spotipy.readthedocs.io/en/latest/#welcome-to-spotipy
    # the paging pattern is slow and delivers unnecessary albums (from compilations and wrong artists)...
    # while results['next']:
    #   results = sp.next(results)
    #   albums.extend(results['items'])

    album_uris = [l['uri'] for l in albums]

    for album_uri in album_uris:
      album = sp.album(album_uri)
      release_date = get_datetime(album['release_date'])
      if acceptable_age_threshold <= release_date:
        sp_counter += 1
        data.append(
            (rel_artist['name'], html.escape(last_fm_artist.get_bio_summary()).replace('\n', '').replace('|', ''),
             album['name'],
             release_date.strftime("%Y-%m-%d")))

    total_count += sp_counter
    print('  ', i, 'of', similar_count, rel_artist['name'], '\t\t\t\t\t\t  Found', sp_counter)

except:
  print("error - usage show_related.py [artist-name]")

print(tabulate(data, ('Artist', 'Bio', 'Album', 'Release Date'), 'pipe'))
print()
print('total count', total_count)


def _get_extracted_from_result_set(result_set):
  result_set = sorted([s.item.name for s in result_set])
  result_text = ', '.join(result_set)
  return result_text
