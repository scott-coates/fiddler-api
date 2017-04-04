from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class SubmitRequest(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, artist_ids, artist_names):
    pass


class SubmitArtistToRequest(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, artist_id, root_artist_id):
    pass

class RefreshPlaylist(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, ):
    pass
