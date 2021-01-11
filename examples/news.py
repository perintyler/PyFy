# -*- encoding: utf-8

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
