# region bootstrap interact
import django
from django.dispatch import receiver

from src.libs.common_domain.domain_command import DomainCommand
from src.tasks import RequestSubmitted1, populate_request

django.setup()

from src.libs.common_domain import aggregate_repository
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.dispatcher import send_command
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.python_utils.objects.object_utils import initializer

request_id = generate_id()


class SubmitRequest(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, artists):
    pass


@receiver(SubmitRequest.command_signal)
def submit_request(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  request = Request.submit(**command.data)
  _aggregate_repository.save(request, -1)




@receiver(RequestSubmitted1.event_signal)
def execute_asset_created_1(**kwargs):
  event = kwargs['event']
  request_id = kwargs['aggregate_id']
  populate_request.delay(request_id, event.artists)


class Request(AggregateBase):
  @classmethod
  def submit(cls, id, artists):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artists:
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artists))

    return ret_val

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.artists = event.artists


artists = """
make war
"""

artists = artists.split('\n')

send_command(-1, SubmitRequest(request_id, artists))

# endregion
