from django.dispatch import receiver

from src.domain.genre.events import GenreCreated1
from src.domain.genre import tasks
from src.libs.common_domain.decorators import event_idempotent
