from django.apps import AppConfig


class MusicDiscoveryConfig(AppConfig):
  name = 'src.apps.music_discovery'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.music_discovery.event_handlers
