from src.domain.request import service
from src.libs.job_utils.job_decorator import job


@job(queue='high')
def create_spotify_playlist_for_request_task(request_id):
  return service.create_spotify_playlist_for_request(request_id)
