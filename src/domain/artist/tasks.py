import logging

from django.core.exceptions import ObjectDoesNotExist

from src.domain.artist import service
from src.domain.artist.commands import CreateArtist, SendAgreementAlerts
from src.domain.artist.entities import Agreement
from src.libs.common_domain import aggregate_repository
from src.libs.common_domain import dispatcher
from src.libs.job_utils.job_decorator import job
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job(queue='high')
def create_artist_task(_aggregate_repo=None, _dispatcher=None, **kwargs):
  if not _aggregate_repo: _aggregate_repo = aggregate_repository
  if not _dispatcher: _dispatcher = dispatcher

  agreement_id = kwargs['aggregate_id']

  # check if already exists - idempotent
  try:

    # pa and agreements share same id
    agreement = _aggregate_repo.get(Agreement, agreement_id)

    logger.debug('Agreement already exists: %s', agreement_id)

    return agreement.id

  except ObjectDoesNotExist:

    log_message = ("Create agreement task for id: %s", agreement_id)

    with log_wrapper(logger.debug, *log_message):
      data = dict({'id': agreement_id}, **kwargs['event'].data)
      create_agreement = CreateArtist(**data)

      _dispatcher.send_command(agreement_id, create_agreement)

@job(queue='high')
def send_alert_for_agreement_task(agreement_id, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher
  log_message = ("Send agreement alert task for id: %s", agreement_id)

  with log_wrapper(logger.debug, *log_message):
    send_alerts_command = SendAgreementAlerts()

    _dispatcher.send_command(agreement_id, send_alerts_command)


@job(queue='high')
def save_agreement_alert_task(agreement_id,
                              outcome_alert_date, outcome_alert_enabled, outcome_alert_created,
                              outcome_notice_alert_date, outcome_notice_alert_enabled, outcome_notice_alert_created,
                              ):
  log_message = ("Create agreement_alert task for agreement_id: %s", agreement_id)

  with log_wrapper(logger.info, *log_message):
    return service.save_agreement_alert(agreement_id,
                                        outcome_alert_date,
                                        outcome_alert_enabled,
                                        outcome_alert_created,
                                        outcome_notice_alert_date,
                                        outcome_notice_alert_enabled,
                                        outcome_notice_alert_created).id


@job(queue='high')
def save_agreement_search_task(agreement_id, user_id, name, counterparty, agreement_type_id):
  log_message = ("Save agreement_search task for agreement_id: %s", agreement_id)

  with log_wrapper(logger.info, *log_message):
    return service.save_agreement_search(agreement_id, user_id, name, counterparty, agreement_type_id).id


@job(queue='high')
def delete_agreement_task(agreement_id):
  log_message = ("Delete agreement_search task for agreement_id: %s", agreement_id)

  with log_wrapper(logger.info, *log_message):
    return service.delete_agreement(agreement_id)
