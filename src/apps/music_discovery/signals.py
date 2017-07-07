from django.dispatch import Signal

from src import domain
from src.domain.common import constants

artist_url_discovered = Signal(providing_args=[constants.URL, constants.ATTRS])
