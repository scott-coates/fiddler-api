import logging

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from tasktiger.schedule import periodic

from src.domain.source.service import source_lookup
from src.libs.job_utils.job_decorator import job

logger = logging.getLogger(__name__)


@job(queue='default')
def create_source_lookup_schedule_task(provider_type, source_type, attrs):
  source_lookup_schedule_task.delay(provider_type, source_type, attrs)
  pass


@job(queue='default', schedule=periodic(days=1, start_date=timezone.now() + relativedelta(days=1)))
def source_lookup_schedule_task(provider_type, source_type, attrs):
  # use tiger code to create periodic task
  # this task is going to call a service --> and that service will interact w/ the source to get new data
  source_lookup_task(provider_type, source_type, attrs)
  pass


@job(queue='default')
def source_lookup_task(provider_type, source_type, attrs):
  source_lookup(provider_type, source_type, attrs)
  pass
