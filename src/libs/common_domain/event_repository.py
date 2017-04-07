from django.db import transaction, IntegrityError

from src.libs.common_domain.errors import ConcurrencyViolationError
from src.libs.common_domain.models import Event


def get_events(event_names=None):
  ret_val = Event.objects.order_by('event_sequence', 'id')

  if event_names:
    ret_val = ret_val.filter(event_name__in=event_names)

  return ret_val


def get_events_for_stream(event_type, stream_id):
  return get_events().filter(event_type=event_type, stream_id=stream_id)


def create_events(stream_id, starting_sequence, event_type, events):
  version = starting_sequence

  with transaction.atomic():
    # the event store had a unique constraint on stream_id and version
    # which handles concurrency conflicts

    event_data = [
      Event(stream_id=stream_id, event_type=event_type, event_name=_get_event_fqn(e), event_sequence=version + i,
            event_data=e.data)
      for i, e in enumerate(events, 1)
      ]

    try:
      events = Event.objects.bulk_create(event_data)
    except IntegrityError as e:
      raise ConcurrencyViolationError(
        'Could not save duplicate events for stream: {0}.'.format(stream_id)).with_traceback(e.__traceback__)

  return events


def delete_events(event_names=None):
  events = Event.objects.order_by('event_sequence', 'id')

  if event_names:
    events = events.filter(event_name__in=event_names)

  events.delete()

  return events


def _get_event_fqn(event):
  return event.__class__.__name__
