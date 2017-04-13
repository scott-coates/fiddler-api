from django.core.management.base import BaseCommand
from tabulate import tabulate

from src.apps.music_discovery.service import get_artist_top_track_albums_data
from src.libs.spotify_utils.spotify_service import get_spotify_id


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('external_ids', nargs='*', default=None)

  def handle(self, *args, **options):
    for spotify_artist_id in options['external_ids']:
      external_artist_id = get_spotify_id(spotify_artist_id)

      top_track_albums_data = get_artist_top_track_albums_data(external_artist_id)
      for top_track_album in top_track_albums_data:
        album_data = top_track_album['album']
        print(tabulate([album_data], headers='keys'))
        print()
        print(tabulate(top_track_album['tracks'], headers='keys', floatfmt='.6f'))
        print()
        print()
        print()
        print()
