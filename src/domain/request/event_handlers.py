from django.dispatch import receiver

from src.domain.request import tasks
from src.domain.request.events import AlbumPromotedToRequest1


@receiver(AlbumPromotedToRequest1.event_signal)
def album_promoted_1(**kwargs):
  event = kwargs['event']

  request_id = kwargs['aggregate_id']

  total_albums_promoted = event.data['total_albums_promoted']

  tasks.update_album_promoted_task.delay(request_id, total_albums_promoted)
