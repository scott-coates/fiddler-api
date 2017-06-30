from django.apps import AppConfig

class EventConfig(AppConfig):
  name = 'src.domain.event'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.event.command_handlers
    import src.domain.event.event_handlers
