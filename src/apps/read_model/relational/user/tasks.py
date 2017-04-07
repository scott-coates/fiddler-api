import logging

from django_rq import job

from src.apps.read_model.relational.user import service
from src.libs.python_utils.logging.logging_utils import log_wrapper
import tasktiger

logger = logging.getLogger(__name__)

#
# @job(queue='high')
# def create_auth_user_task(id, email):
#   log_message = ("Save user task for email: %s", email)
#
#   with log_wrapper(logger.info, *log_message):
#     return service.save_auth_user(id, email).id
