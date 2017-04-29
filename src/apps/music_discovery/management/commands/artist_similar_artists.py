import operator
from pprint import pprint

from django.core.management.base import BaseCommand
from tabulate import tabulate

from src.apps.music_discovery.service import get_artist_top_track_albums_data, _get_lfm_artist_by_name
from src.libs.spotify_utils.spotify_service import get_spotify_id


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('artist_names', nargs='*', default=None)

  def handle(self, *args, **options):
    for artist_name in options['artist_names']:
      lfm_artist = _get_lfm_artist_by_name(artist_name)
      similar_artists = lfm_artist.get_similar(100)
      similar_artist_names = sorted([a.item.name for a in similar_artists], key=str.lower)
      print('Similar for', lfm_artist.get_name())
      pprint(similar_artist_names)
