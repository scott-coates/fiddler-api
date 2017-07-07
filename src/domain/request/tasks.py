from tasktiger import linear

from src.domain.request import service
from src.domain.request.commands import RefreshPlaylist
from src.libs.common_domain import dispatcher
from src.libs.job_utils.job_decorator import job


@job(queue='high')
def create_spotify_playlist_for_request_task(request_id):
  return service.create_spotify_playlist_for_request(request_id)


@job(queue='high', retry=True, retry_method=linear(5, 5, 10))
def refresh_request_playlist_task(request_id):
  refresh = RefreshPlaylist()
  dispatcher.send_command(request_id, refresh)
