import os
import dotenv

import pyty
from pyty import IS, List

dotenv.load_dotenv()

CLIENT_ID  = os.getenv('SPOTIFY_CLIENT_ID')
SECRET_KEY = os.getenv('SPOTIFY_SECRET_KEY')

URI = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

api = pyty.Api(URI)
api.request_token(CLIENT_ID, SECRET_KEY, authUrl=AUTH_URL)
# api.add_endpoint(Endpoint())

class Songs(pyty.Schema):
  name:       str
  explicit:   bool
  popularity: int

@endpoint.GET(api, '/artists/top', name='fetch_all')
class Artist(pyty.Schema):
  id:     int
  name:   str
  genres: List[str]
  tracks: List[Song] = 'alias'   |IS| 'songs' \
                   and 'default' |IS| []

for artist in Artist.fetch_all():
  for song in artist.songs:
    print(song.name)

if __name__ == '__main__':
  pass
