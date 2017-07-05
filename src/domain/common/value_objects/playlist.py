class Playlist:
  def __init__(self, provider_type, external_id, track_ids=None):
    self.provider_type = provider_type
    self.external_id = external_id
    self.track_ids = track_ids or []

  def __str__(self):
    return 'Playlist: {id}'.format(id=self.external_id)
