from django.core.management.base import BaseCommand
from tabulate import tabulate

from src.apps.maintenance.database.service import clear_tiger_jobs
from src.apps.music_discovery.service import get_artist_top_track_albums_data, get_flat_track_data_by_external
from src.libs.common_domain import event_store
from src.libs.spotify_utils.spotify_service import get_spotify_id


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('external_ids', nargs='*', default=None)

  def handle(self, *args, **options):
    for spotify_track_id in options['external_ids']:
      external_track_id = get_spotify_id(spotify_track_id)
      track_data = get_flat_track_data_by_external(external_track_id)
      print(tabulate([track_data], headers='keys', floatfmt='.6f'))
      print()
      print()
