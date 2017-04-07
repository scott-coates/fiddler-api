import os
import sys

import tasktiger
from django.core.management.base import BaseCommand
from redis import Redis


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('event_names', nargs='*', default=None)

  def handle(self, *args, **options):
    try:
      command = sys.argv[1]
    except IndexError:
      command = None

    if command == 'tasktiger':
      # Strip the "tasktiger" arg when running via manage, so we can run e.g.
      # ./manage.py tasktiger --help

      # http://stackoverflow.com/questions/36651680/click-will-abort-further-execution-because-python-3-was-configured-to-use-ascii
      os.environ.setdefault('LC_ALL', 'en_US.utf-8')
      os.environ.setdefault('LANG', 'en_US.utf-8')

      conn = Redis(db=2, decode_responses=True)
      tiger = tasktiger.TaskTiger(connection=conn, setup_structlog=True)
      tiger.run_worker_with_args(sys.argv[2:])
      sys.exit(0)
