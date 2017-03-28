from src.libs.python_utils.types.type_utils import load_relative_object


def load_domain_event_from_event_record(event_record, aggregate_class):
  event_name = event_record.event_name
  event_data = event_record.event_data

  domain_event_class = load_relative_object(aggregate_class, '.events', event_name)

  try:
    domain_event = domain_event_class.hydrate(**event_data)
  except Exception as e:
    raise Exception('Unable to load events for event: {0}.'.format(event_record)).with_traceback(e.__traceback__)

  return domain_event
