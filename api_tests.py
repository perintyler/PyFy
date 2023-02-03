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


"""
Example Usage of PyTy for the News API

https://newsapi.org/docs/get-started
"""

import pyty

URI = 'http://newsapi.org/v2'
API_KEY = '<NEWS-API-KEY>'

newsApi = pyty.Api(URI)
newsApi.set_key(NEWS_API_KEY)

@pyty.endpoint.GET(newsApi, '/everything', params={'q': "Cote d'Ivoire"}, alias='get_all')
class Article(pyty.Schema):
  source: dict # {id,name}
  author: str
  title: str
  url: pyty.Url

for article in Article.get_all():
  print(article.title)


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
