from django.core.management.base import BaseCommand
from tabulate import tabulate

from src.apps.music_discovery.service import get_flat_track_data_by_internal
from src.domain.request.entities import Request
from src.libs.common_domain import aggregate_repository


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('request_ids', nargs='*', default=None)

  def handle(self, *args, **options):
    for request_id in options['request_ids']:

      request = aggregate_repository.get(Request, request_id)
      tids = request.playlist.track_ids

      playlist_track_data = []

      for tid in tids:
        track_data = get_flat_track_data_by_internal(tid)
        playlist_track_data.append(track_data)

      print(tabulate(playlist_track_data, headers='keys', floatfmt='.6f'))
      print()
      print()
      print()
