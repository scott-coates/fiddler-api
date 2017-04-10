import random

import tasktiger
# delay_sec will be different for each instance of tiger
from tasktiger.retry import fixed

from src.libs.key_value_utils.key_value_provider import get_key_value_client

delay_sec = random.choice(range(5, 20))
retries = 5


def job(**kwargs):
  def _wrap(func):
    conn = get_key_value_client()

    tiger = tasktiger.TaskTiger(connection=conn)

    extended_retry = kwargs.pop('extended_retry', None)
    if extended_retry:
      kwargs['retry'] = True
      kwargs['retry_method'] = fixed(delay_sec, retries)

    return tiger.task(**kwargs)(func)

  return _wrap
