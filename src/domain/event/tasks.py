import logging

from django.core.exceptions import ObjectDoesNotExist

from src.domain.event import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job(queue='high')
def create_asset_lookup_task(asset_id, name, path):
  # check if already exists - idempotent
  try:
    at = service.get_asset_lookup(asset_id)
    logger.debug('UserAgreementType already exists: %s', asset_id)

    return at.id

  except ObjectDoesNotExist:
    log_message = ("Create user asset_lookup task for asset_id: %s", asset_id)

    with log_wrapper(logger.info, *log_message):
      return service.create_asset_lookup(asset_id, name, path).id
