from importlib import import_module


# https://github.com/scrapy/scrapy/blob/master/scrapy/utils/misc.py
def load_relative_object(_class, relative_mod, name):
  """Load an object given its absolute object path, and return it.

  object can be a class, function, variable o instance.
  path ie: 'scrapy.contrib.downloadermiddelware.redirect.RedirectMiddleware'
  """

  module = import_module(relative_mod, import_module(_class.__module__).__package__)
  obj = getattr(module, name)

  return obj
