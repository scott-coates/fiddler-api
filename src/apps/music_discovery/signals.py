from django.dispatch import Signal

from src.domain.common import constants

artist_url_discovered = Signal(providing_args=[constants.NAME, constants.URL, constants.ATTRS])
