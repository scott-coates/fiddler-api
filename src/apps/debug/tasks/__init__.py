import logging

from src.libs.job_utils.job_decorator import job

logger = logging.getLogger(__name__)



@job(queue='high')
def test(a='world'):
  logger.debug('hello, %s!', a)
