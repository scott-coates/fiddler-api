from django.dispatch import receiver

from src.domain.source import tasks
from src.domain.source.events import SourceCreated1


@receiver(SourceCreated1.event_signal)
def source_created_1(**kwargs):
  event = kwargs['event']

  provider_type = event.data['provider_type']
  source_type = event.data['source_type']
  attrs = event.data['attrs']

  tasks.create_source_lookup_schedule_task.delay(provider_type, source_type, attrs)

  # execuite it now
  tasks.source_lookup_task.delay(provider_type, source_type, attrs)
