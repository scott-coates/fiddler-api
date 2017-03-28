from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.domain.request.events import RequestSubmitted1, AlbumAddedToRequest1
from src.libs.common_domain.aggregate_base import AggregateBase

acceptable_age_threshold = timezone.now() - relativedelta(months=500)


class Request(AggregateBase):
  def __init__(self):
    super().__init__()
    self.albums = []

  @classmethod
  def submit(cls, id, artists):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    if not artists or not all(artists):
      raise TypeError("artists is required")

    ret_val._raise_event(RequestSubmitted1(id, artists))

    return ret_val

  def add_album(self, album_id, release_date, artist_id):
    if acceptable_age_threshold <= release_date:
      self._raise_event(AlbumAddedToRequest1(album_id, artist_id))

  def _handle_submitted_1_event(self, event):
    self.id = event.id
    self.artists = event.artists

  def _handle_album_added_1_event(self, event):
    self.albums.append(event.album_id)

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
