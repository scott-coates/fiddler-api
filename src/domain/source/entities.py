from src.domain.source.events import SourceCreated1

from src.libs.common_domain.aggregate_base import AggregateBase


class Source(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, source_type, attrs):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    ret_val._raise_event(SourceCreated1(id, name, source_type, attrs))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.source_type = event.source_type
    self.attrs = event.attrs

  def __str__(self):
    return 'Source {id}: {name}'.format(id=self.id, name=self.name)
