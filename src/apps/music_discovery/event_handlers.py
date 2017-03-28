from django.dispatch import receiver

from src.apps.music_discovery import tasks
from src.domain.request.events import RequestSubmitted1


@receiver(RequestSubmitted1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  artists = event.data['artists']
  r_id = kwargs['aggregate_id']

  for artist_name in artists:
    tasks.discover_music_for_request_task.delay(r_id, artist_name)
