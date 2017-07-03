from django.apps import AppConfig


class PlaylistConfig(AppConfig):
  name = 'src.domain.playlist'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.playlist.command_handlers
    import src.domain.playlist.event_handlers
