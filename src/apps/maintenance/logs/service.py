import glob
import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from src.libs.key_value_utils.key_value_provider import get_key_value_client


def clear_log_files():
  app_root = os.path.dirname(settings.DJANGO_ROOT)
  log_path = os.path.join(app_root, 'logs', '*.log*')
  for f in glob.glob(log_path):
    os.remove(f)


