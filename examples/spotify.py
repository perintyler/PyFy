# -*- encoding: utf-8

"""
Example Usage of PyTy for the Spotify API

https://developer.spotify.com/documentation/web-api/quick-start/
"""
###############################################################################
# Some spotify auth stuff. Skip to next section for PyTy usage. I plan on
# providing lib support for authentication soon,
###############################################################################

import pyty
from pyty import IS, List

CLIENT_ID  = '<SPOTIFY-API-KEY>'
SECRET_KEY = '<SPOTIFY-API-KEY>'
URI = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

api = pyty.Api(URI)
api.request_token(CLIENT_ID, SECRET_KEY, authUrl=AUTH_URL)

class Track(pyty.Schema):
  id:         str = 'required'
  name:       str
  explicit:   bool
  popularity: int =   'default' |IS|  0      \
                  and 'range'   |IS| (0,100) \
                  and 'alias'   |IS| 'score'

@endpoint.GET(URI, 'artists/', name='fetch_all')
class Artist(pyty.Schema):
  id: int = 'required'
  name: str
  genres: List[str]
  tracks: List[Track] = 'endpoint' |IS| 'get_tracks'

for artist in Artist.fetch_all():
  for song in artist.songs:
    print(song.name)
