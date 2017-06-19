from src.domain.genre.events import GenreCreated1

from src.libs.common_domain.aggregate_base import AggregateBase


class Genre(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, provider_type, external_id):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    ret_val._raise_event(GenreCreated1(id, name, provider_type, external_id))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.provider_type = event.provider_type
    self.external_id = event.external_id

  def __str__(self):
    return 'Genre {id}: {name}'.format(id=self.id, name=self.name)
