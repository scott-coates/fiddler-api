import logging

from src.apps.read_model.key_value.genre import service
from src.apps.read_model.key_value.genre.service import add_unique_track_id
from src.libs.datetime_utils.datetime_parser import get_datetime
from src.libs.job_utils.job_decorator import job

logger = logging.getLogger(__name__)

@job(queue='high')
def set_album_external_id_task(album_id, name, popularity, release_date, provider_type, external_id):
  release_date = get_datetime(release_date)
  return service.set_album_info(album_id, name, popularity, release_date, provider_type, external_id)


@job(queue='high')
def set_album_id_task(album_id, provider_type, external_id):
  return service.set_album_id(album_id, provider_type, external_id)


@job(queue='high')
def add_album_to_genre_task(album_id, genre_id):
  return service.add_album_to_genre(album_id, genre_id)


@job(queue='high')
def add_track_to_album_task(album_id, track_data):
  return service.add_track_to_album(album_id, track_data)


@job(queue='high')
def save_track_info_task(track_id, track_data, album_id):
  return service.save_track_info(track_id, track_data, album_id)


@job(queue='high')
def set_track_external_id_task(track_id, provider_type, external_id):
  return service.set_track_external_id(track_id, provider_type, external_id)


@job(queue='high')
def add_external_genre_id_task(genre_id, provider_type, external_id):
  return service.add_external_genre_id(genre_id, provider_type, external_id)


@job(queue='high')
def add_unique_genre_id_task(genre_id, provider_type, external_id):
  return service.add_unique_genre_id(genre_id, provider_type, external_id)


@job(queue='high')
def save_genre_info_task(genre_id, name, genres, popularity):
  return service.save_genre_info(genre_id, name, genres, popularity)


@job(queue='high')
def save_genre_top_tracks_task(genre_id, track_data):
  return service.save_genre_top_tracks(genre_id, track_data)


@job(queue='high')
def add_unique_track_id_task(track_id, provider_type, external_id):
  return add_unique_track_id(track_id, provider_type, external_id)
