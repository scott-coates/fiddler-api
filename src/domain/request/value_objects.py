class SpotifyPlaylist:
  def __init__(self, playlist_id, tracks=None):
    self.playlist_id = playlist_id
    self.tracks = tracks or []

  def __str__(self):
    return 'SpotifyPlaylist: {id}'.format(id=self.playlist_id)
