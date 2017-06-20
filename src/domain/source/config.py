from django.apps import AppConfig


class SourceConfig(AppConfig):
  name = 'src.domain.source'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.source.command_handlers
    import src.domain.source.event_handlers
