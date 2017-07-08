from django.dispatch import receiver

from src.apps.read_model.key_value.event import tasks
from src.domain.event.events import ArtistAssociated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ArtistAssociated1.event_signal)
def artist_associated_1(**kwargs):
  event = kwargs['event']

  request_id = kwargs['aggregate_id']
  artist_id = event.data['artist_id']

  tasks.process_artist_event_task.delay(request_id, artist_id)
