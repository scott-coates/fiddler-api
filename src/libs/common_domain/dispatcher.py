import logging

from src.libs.common_domain.errors import ConcurrencyViolationError

logger = logging.getLogger(__name__)

command_try_times = 100


# these two methods should probably be split. their signatures may change throughout the future.
def send_command(aggregate_id, command):
  command_counter = 1
  command_data = {'aggregate_id': aggregate_id, 'command': command}

  error = None

  while command_counter <= command_try_times:
    try:
      command.__class__.command_signal.send(None, **command_data)
    except ConcurrencyViolationError as e:
      logger.info('Concurrency error for aggregate: %s. Command: %s. Attempt no. %s.', aggregate_id, command,
                  command_counter)
      error = e
      command_counter += 1
    else:
      # successful command, break the loop
      error = None
      break

  if error: raise error


def publish_event(aggregate_id, event, version, allow_non_idempotent, send_to_app_names):
  event_data = {'aggregate_id': aggregate_id, 'event': event, 'version': version}
  event.__class__.event_signal.send(None, allow_non_idempotent, send_to_app_names, **event_data)
