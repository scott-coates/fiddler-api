from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreateArtist(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, provider_type, external_id):
    pass


class CreateAlbum(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, release_date, provider_type, external_id, artist_id):
    pass

class AddTracks(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, track_data):
    pass