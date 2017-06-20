from django.dispatch import receiver

from src.domain.source import tasks
from src.domain.source.events import SourceCreated1


@receiver(SourceCreated1.event_signal)
def source_created_1(**kwargs):
  event = kwargs['event']

  source_id = kwargs['aggregate_id']
  name = event.data['name']
  source_type = event.data['source_type']
  attrs = event.data['attrs']

  tasks.create_source_lookup_schedule_task.delay(source_id, name, source_type, attrs)
