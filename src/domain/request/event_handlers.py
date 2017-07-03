from django.dispatch import receiver

from src.domain.request.events import RequestSubmitted1
from src.domain.request import tasks


@receiver(RequestSubmitted1.event_signal)
def create_playlist_for_request(**kwargs):
  request_id = kwargs['aggregate_id']

  tasks.create_playlist_for_request_task(request_id)
