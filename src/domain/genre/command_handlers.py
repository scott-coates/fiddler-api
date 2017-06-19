from django.dispatch import receiver

from src.apps.read_model.key_value.genre.service import add_unique_genre_id, clear_unique_genre_id
from src.domain.genre.commands import CreateGenre
from src.domain.genre.entities import Genre
from src.domain.genre.errors import DuplicateGenreError
from src.libs.common_domain import aggregate_repository


@receiver(CreateGenre.command_signal)
def create_agreement(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  newly_added = add_unique_genre_id(kwargs['aggregate_id'], command.data['provider_type'], command.data['external_id'])

  if not newly_added: raise DuplicateGenreError('genre: ', command.id, 'already exists.')

  try:
    genre = Genre.from_attrs(**command.data)
    _aggregate_repository.save(genre, -1)
  except:
    # it's possible this line is never hit, causing us to have to manually fix the issue
    clear_unique_genre_id(command.data['provider_type'], command.data['external_id'])
    raise
