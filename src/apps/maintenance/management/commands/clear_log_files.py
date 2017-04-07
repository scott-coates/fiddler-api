from django.core.management.base import BaseCommand

from src.apps.maintenance.logs.service import clear_log_files


class Command(BaseCommand):
  def handle(self, *args, **options):
    clear_log_files()
