from django.dispatch import receiver

from src.domain.common import constants
from src.domain.event.events import EventCreated1
from src.domain.source import tasks
from src.domain.source.commands import CreateSource
from src.domain.source.events import SourceCreated1
from src.libs.common_domain import aggregate_repository
from src.libs.common_domain.dispatcher import send_command
from src.libs.python_utils.id.id_utils import generate_id


@receiver(SourceCreated1.event_signal)
def source_created_1(**kwargs):
  event = kwargs['event']

  provider_type = event.data['provider_type']
  source_type = event.data['source_type']
  attrs = event.data['attrs']

  tasks.create_source_lookup_schedule_task.delay(provider_type, source_type, attrs)

  # execuite it now
  tasks.source_lookup_task.delay(provider_type, source_type, attrs)


@receiver(EventCreated1.event_signal)
def create_source_from_event(**kwargs):
  event = kwargs['event']
  music_event_url = event.attrs[constants.URL]

  source_attrs = {
    'entity_type': 'event',
    'entity_id': event.id,
    constants.URL: music_event_url,
  }

  source_id = generate_id()

  if 'mileofmusic' in music_event_url.lower():
    provider_type = 'mile-of-music'
  else:
    raise Exception('invalid event type', music_event_url)

  send_command(-1, CreateSource(
    source_id, event.name,
    provider_type, constants.WEBSITE,
    source_attrs
  ))
