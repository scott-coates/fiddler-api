from django.dispatch import receiver

from src.domain.event.commands import CreateEvent
from src.domain.event.entities import Event
from src.libs.common_domain import aggregate_repository


@receiver(CreateEvent.command_signal)
def create_event(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Event.from_attrs(**command.data)
  _aggregate_repository.save(request, -1)
