from src.domain.playlist import service
from src.libs.job_utils.job_decorator import job


@job(queue='high')
def create_external_playlist_task(playlist_id, playlist_name):
  return service.create_external_playlist(playlist_id, playlist_name)
