from src.domain.common import constants


def source_lookup(source_id, name, source_type, attrs):
  url = attrs[constants.URL]
  # use tiger code to create periodic task
  # this task is going to call a service --> and that service will interact w/ the source to get new data
  pass
