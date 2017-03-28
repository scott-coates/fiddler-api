from src.libs.python_utils.types.type_utils import load_object


def load_domain_event_from_event_record(event_record):
  event_type = event_record.event_type
  event_name = event_record.event_name
  event_data = event_record.event_data

  event_fqn = 'src.domain.{0}.events.{1}'.format(event_type.lower(), event_name)
  domain_event_class = load_object(event_fqn)

  try:
    domain_event = domain_event_class.hydrate(**event_data)
  except Exception as e:
    raise Exception('Unable to load events for event: {0}.'.format(event_record)).with_traceback(e.__traceback__)

  return domain_event
