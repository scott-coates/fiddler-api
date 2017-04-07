import random

import tasktiger
from redis import Redis

# delay_sec will be different for each instance of tiger
from tasktiger.retry import fixed

delay_sec = random.choice(range(5, 20))


def job(**kwargs):
  def _wrap(func):
    conn = Redis(db=2, decode_responses=True)
    tiger = tasktiger.TaskTiger(connection=conn)

    extended_retry = kwargs.pop('extended_retry', None)
    if extended_retry:
      kwargs['retry'] = True
      kwargs['retry_method'] = fixed(delay_sec, 50)

    return tiger.task(**kwargs)(func)

  return _wrap
