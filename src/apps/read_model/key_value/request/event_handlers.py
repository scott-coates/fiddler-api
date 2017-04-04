from django.dispatch import receiver

from src.apps.read_model.key_value.request import tasks
from src.domain.request.events import ArtistPromotedToRequest1, ArtistSkippedByRequest1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ArtistPromotedToRequest1.event_signal)
@receiver(ArtistSkippedByRequest1.event_signal)
def album_promoted_1(**kwargs):
  event = kwargs['event']

  request_id = kwargs['aggregate_id']

  tasks.incr_artist_promoted_task.delay(request_id)
