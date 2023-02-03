# -*- coding: utf-8 -*-

"""
pyty.api
~~~~~~~~

This module provides support for retrieving codable data from REST APIs.
"""

# REST
import requests

# PyTy modules
from .utils import *
from .exceptions import *

def make_request(method, url, **kwargs):
  """Send REST request

  Raises ApiException if response is bad.

  :param method[str]: REST request method e.g. GET, PUT, etc.
  :param \*\*kwargs: (optional) these get passed into the requests lib function
  :rtype dict: the parsed json from the response
  """
  request = getattr(requests, method.lower(), None) # i.e. 'GET' -> requests.get
  if not requests:
    raise ApiException('Invalid Request Method')

  resp = request(url, **kwargs)
  if resp.status_code != 200:
    print(method, url, resp.status_code, kwargs, '\n', resp.content)
    raise ApiException('bad status code')

  return resp.json()

def codable_endpoint(method, name, api, path, **options):
  """Decorator for a `Codable` subclass.

  A Codable subclass decorated with this function will be able to
  hit the endpoint as a class method like this. Don't use this function
  directly. Instead, use `pyty.api.endpoints`.

  :param method[str]: request method (GET, POST, etc.)
  :param name[str]: what to name the function that will return the encoded endpoint response
  :param api[Api]: this gets assigned the function that can return an enpoint's encoded data
  :param path[str]: path of the endpoint to hit (after URI)
  :param \*\*options[dict]: (optional) these get passed into the requests lib function
  :rtype func->Codable: the wrapped 'Codable' type decorated by this function.
                        The endpoint will now be accessible as a class method.
  """
  def request_wrapper(cls):

    def encode_response():
      response = make_request(method, api.get_url(endpoint), **options)
      return cls.encode(response)

    setattr(api, name, encode_response)
    return cls

  return request_wrapper

class endpoints:
  """Encapsulates an endpoint decorator for each of the request method.

  Example Usage:
  >>> @endpoint.GET(api, 'fetch_users', '/users')
  >>> class User(Schema):
  >>>   ...
  >>> users = User.fetch_users()
  """
  # todo: add the rest of the request methods
  def GET(*args,**kwargs):      codable_endpoint('GET', *args, **kwargs)
  def PUT(*args,**kwargs):      codable_endpoint('PUT', *args, **kwargs)
  def POST(*args,**kwargs):     codable_endpoint('POST', *args, **kwargs)
  def PATCH(*args,**kwargs):    codable_endpoint('PATCH', *args, **kwargs)
  def DELETE(*args,**kwargs):   codable_endpoint('DELETE', *args, **kwargs)
  def OPTIONS(*args,**kwargs):  codable_endpoint('OPTIONS', *args, **kwargs)

class Api:
  """Provides functionality to interact with an API.

  The endpoint decorator assigns functions to an `Api` object which can
  be used to fetch encoded response from that endpoint.
  """

  def __init__(self, uri):
    self.uri       = uri
    self.authMode  = None
    self.token     = None
    self.key       = None
    self.authUser  = None
    self.endpoints = []

  def get_url(self, endpoint):
    uri,path = self.uri,endpoint
    if path.startswith('/'): path = path[1:]
    if uri.endswith('/'):    uri  = path[:-1]
    return f'{uri}/{path}'

  def request_token(self, clientId, secretKey, authEndpoint=None, authUrl=None):
    """OAuth 2.0 Token Protocol: https://tools.ietf.org/html/rfc6749#section-4.4"""
    if authEndpoint is None and authUrl is None:
      raise ApiException('Either an auth endpoint path or url must be provided')
    url = authUrl if authEndpoint is None else f'{self.uri}/{authEndpoint}'
    self.token = make_request('POST', url, headers={
      'grant_type': 'client_credentials',
      'client_id': clientId,
      'client_secret': secretKey,
    })['access_token']
    self.authMode = 'TOKEN'

  def set_api_key(self, key):
    self.authMode = 'KEY'
    self.key = key

  def set_auth_user(self, user):
    # TODO
    pass
