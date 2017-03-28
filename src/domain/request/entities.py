from src.domain.request.events import SmartViewCreated1, SmartViewNameChanged1, SmartViewQueryChanged1, \
  RequestSubmitted1
from src.libs.common_domain.aggregate_base import AggregateBase


class Request(AggregateBase):
  @classmethod
  def submit(cls, id, artists):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artists or not all(artists):
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artists))

    return ret_val

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.artists = event.artists

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
