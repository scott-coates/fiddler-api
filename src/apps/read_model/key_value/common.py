_read_model_prefix = 'read_model'
_app_prefix = 'app'


def get_read_model_name(key_name, *args, **kwargs):
  ret_val = _get_prefix(key_name, _read_model_prefix, *args, **kwargs)

  return ret_val


def get_app_name(key_name, *args, **kwargs):
  ret_val = _get_prefix(key_name, _app_prefix, *args, **kwargs)

  return ret_val


def _get_prefix(key_name, prefix, *args, **kwargs):
  key_name = key_name.format(*args, **kwargs)

  ret_val = '{0}:{1}'.format(prefix, key_name)

  return ret_val
