from django.dispatch import receiver

from src.apps.read_model.key_value.artist import tasks
from src.domain.artist.events import AlbumAddedToArtist1, TrackAddedToAlbum1, ArtistCreated1, TopTracksRefreshed1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ArtistCreated1.event_signal)
def execute_artist_created_1(**kwargs):
  event = kwargs['event']
  artist_id = kwargs['aggregate_id']
  genres = event.data['genres']
  popularity = event.data['popularity']
  tasks.save_artist_info_task.delay(artist_id, genres, popularity, )
  tasks.add_external_artist_id_task(artist_id, event.data['provider_type'], event.data['external_id'])
  tasks.add_unique_artist_id_task(artist_id, event.data['provider_type'], event.data['external_id'])


@event_idempotent
@receiver(AlbumAddedToArtist1.event_signal)
def execute_prospect_deleted_1(**kwargs):
  event = kwargs['event']
  artist_id = kwargs['aggregate_id']

  album_id = event.data['id']
  name = event.data['name']
  popularity = event.data['popularity']
  release_date = str(event.data['release_date'])
  provider_type = event.data['provider_type']
  external_id = event.data['external_id']
  tasks.set_album_external_id_task.delay(album_id, name, popularity, release_date, provider_type, external_id)
  tasks.set_album_id_task.delay(album_id, provider_type, external_id)
  tasks.add_album_to_artist_task.delay(album_id, artist_id)


@event_idempotent
@receiver(TrackAddedToAlbum1.event_signal)
def execute_track_1(**kwargs):
  event = kwargs['event']

  id = event.data['id']
  name = event.data['name']
  popularity = event.data['popularity']
  features = event.data['features']
  provider_type = event.data['provider_type']
  external_id = event.data['external_id']

  album_id = event.data['album_id']

  track_data = {'id': id, 'name': name, 'popularity': popularity, 'features': features, 'provider_type': provider_type,
                'external_id': external_id}

  tasks.add_track_to_album_task.delay(album_id, track_data)
  tasks.set_track_external_id_task.delay(id, provider_type, external_id)
  tasks.add_unique_track_id_task.delay(id, provider_type, external_id)
  tasks.save_track_info_task.delay(id, track_data, album_id)


@event_idempotent
@receiver(TopTracksRefreshed1.event_signal)
def refreshed_top_tracks_1(**kwargs):
  event = kwargs['event']

  artist_id = kwargs['aggregate_id']
  track_data = event.data['track_data']

  tasks.save_artist_top_tracks_task.delay(artist_id, track_data)


  #
  # @event_idempotent
  # @receiver(EngagementOpportunityAddedToProfile1.event_signal)
  # def execute_added_eo_1(**kwargs):
  #   aggregate_id = kwargs['aggregate_id']
  #   event = kwargs['event']
  #
  #   attrs = event.attrs
  #
  #   tasks.save_recent_eo_content_task.delay(
  #       event.id, attrs, event.external_id,
  #       event.provider_type, event.provider_action_type, aggregate_id
  #   )
  #
  #
  # @event_idempotent
  # @receiver(EngagementOpportunityAddedToProfile1.event_signal)
  # def execute_added_eo_save_discovery_network_1(**kwargs):
  #   aggregate_id = kwargs['aggregate_id']
  #   event = kwargs['event']
  #
  #   attrs = event.attrs
  #
  #   provider_type = event.provider_type
  #   prospect_id = aggregate_id
  #
  #   tasks.save_recent_prospect_discovery_network_connections_from_eo_task.delay(
  #       attrs, provider_type, prospect_id
  #   )
