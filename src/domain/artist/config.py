from django.apps import AppConfig


class ArtistConfig(AppConfig):
  name = 'src.domain.artist'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.artist.command_handlers
    import src.domain.artist.event_handlers
