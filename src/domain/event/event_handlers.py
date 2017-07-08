from django.dispatch import receiver

from src.domain.event import tasks
from src.domain.event.events import EventCreated1


@receiver(EventCreated1.event_signal)
def event_created(**kwargs):
  event_id = kwargs['aggregate_id']

  tasks.create_spotify_playlist_for_event_task.delay(event_id)
