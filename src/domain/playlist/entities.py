import logging

from src.domain.playlist.errors import PlaylistExistsError
from src.domain.playlist.events import PlaylistCreated1, ExternalPlaylistGenerated1
from src.libs.common_domain.aggregate_base import AggregateBase

logger = logging.getLogger(__name__)


class Playlist(AggregateBase):
  def __init__(self):
    super().__init__()
    self.name = None
    self.provider_type = None
    self.external_id = None
    self.external_url = None

  @classmethod
  def from_attrs(cls, id, name, entity_type, entity_id):
    ret_val = cls()
    if not id:
      raise TypeError("id is required")

    ret_val._raise_event(PlaylistCreated1(id, name, entity_type, entity_id))

    return ret_val

  @property
  def spotify_playlist_url(self):
    return self.external_id

  def set_external_playlist_info(self, name, provider_type, external_id, external_url):
    assert name
    assert provider_type
    assert external_id
    assert external_url

    # this prevents the same root artist submitting the same potential artist
    if self.external_id:
      raise PlaylistExistsError(f'playlist: {self.external_id} already exists')

    self._raise_event(ExternalPlaylistGenerated1(name, provider_type, external_id, external_url))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.entity_type = event.entity_type
    self.entity_id = event.entity_id

  def _handle_external_playlist_generated_1_event(self, event):
    self.name = event.data['name']
    self.provider_type = event.data['provider_type']
    self.external_id = event.data['external_id']
    self.external_url = event.data['external_url']

  def __str__(self):
    class_name = self.__class__.__name__
    return '{class_name}: {id}'.format(class_name=class_name, id=self.id, )
