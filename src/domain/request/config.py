from django.apps import AppConfig


class RequestConfig(AppConfig):
  name = 'src.domain.request'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.request.command_handlers
    import src.domain.request.event_handlers
