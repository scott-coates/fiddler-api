from django.apps import AppConfig

class GenreConfig(AppConfig):
  name = 'src.domain.genre'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.genre.command_handlers
    import src.domain.genre.event_handlers
