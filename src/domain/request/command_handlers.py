from django.dispatch import receiver

from src.debug_file import SubmitRequest
from src.domain.request.entities import Request
from src.libs.common_domain import aggregate_repository


@receiver(SubmitRequest.command_signal)
def submit_request(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Request.submit(**command.data)
  _aggregate_repository.save(request, -1)
