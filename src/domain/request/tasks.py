from django_rq import job

from src.domain.request import service


@job('high')
def update_album_promoted_task(request_id, total_albums_promoted):
  return service.update_album_promoted(request_id, total_albums_promoted)
