from django.dispatch import receiver

from src.domain.request import tasks
from src.domain.request.events import RequestSubmitted1


@receiver(RequestSubmitted1.event_signal)
def request_submitted(**kwargs):
  request_id = kwargs['aggregate_id']

  tasks.create_spotify_playlist_for_request_task.delay(request_id)
