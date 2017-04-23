import random

# delay_sec will be different for each instance of tiger
from tasktiger.retry import fixed

from src.libs.job_utils.shared_tiger_connection import get_shared_tiger_connection

delay_sec = random.choice(range(5, 20))
retries = 5


def job(**kwargs):
  def _wrap(func):
    tiger = get_shared_tiger_connection()

    extended_retry = kwargs.pop('extended_retry', None)
    if extended_retry:
      kwargs['retry'] = True
      kwargs['retry_method'] = fixed(delay_sec, retries)

    return tiger.task(**kwargs)(func)

  return _wrap
