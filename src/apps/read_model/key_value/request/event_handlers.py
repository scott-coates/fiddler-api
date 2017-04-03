from django.dispatch import receiver

from src.apps.read_model.key_value.artist import tasks
from src.domain.artist.events import AlbumAddedToArtist1, TrackAddedToAlbum1, ArtistCreated1, TopTracksRefreshed1
from src.domain.common import constants

from src.libs.common_domain.decorators import event_idempotent

