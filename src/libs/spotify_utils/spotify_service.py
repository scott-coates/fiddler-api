def get_spotify_id(spotify_id):
  fields = spotify_id.split(':')
  return fields[-1]
