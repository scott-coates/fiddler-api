from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreatePlaylist(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, entity_type, entity_id):
    pass


class ProvideExternalPlaylist(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, name, provider_type, external_id, external_url):
    pass
