from django.dispatch import receiver

from src.domain.source.commands import CreateSource
from src.domain.source.entities import Source
from src.libs.common_domain import aggregate_repository


@receiver(CreateSource.command_signal)
def create_potential_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Source.from_attrs(**command.data)
  _aggregate_repository.save(request, -1)
