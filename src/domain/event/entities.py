from src.domain.event.events import EventCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Event(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, attrs):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not attrs:
      raise TypeError("attrs is required")

    ret_val._raise_event(EventCreated1(id, name, attrs))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.attrs = event.attrs

  def __str__(self):
    return 'Event{id}: {name}'.format(id=self.id, name=self.name)
