class SpotifyPlaylist:
  def __init__(self, playlist_id):
    self.playlist_id = playlist_id

  def __str__(self):
    return 'SpotifyPlaylist: {id}'.format(id=self.playlist_id)
