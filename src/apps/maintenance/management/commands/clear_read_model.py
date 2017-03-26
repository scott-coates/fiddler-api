from django.core.management.base import BaseCommand

from src.apps.maintenance.database.service import clear_read_model


class Command(BaseCommand):
  def handle(self, *args, **options):
    clear_read_model()
