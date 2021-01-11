# PyTy

PyTy is a library that provides support for interacting with APIs by offering a quick and easy way to create objects that represent data from an API endpoint. Type safety is a feature and encodable schemas can be defined to validate REST responses.

### **This is a Work In Progress**

## Installing
todo: make pip package

## Example Usage

```
>>> from pyty import Schema, Api, IS, List
>>>
>>> api = pyty.Api('<API-URI>')
>>> api.request_token('<CLIENT-ID>', '<SECRET-KEY>', authUrl = AUTH_URL)
>>>
>>> class Songs(pyty.Schema):
>>>   name:       str
>>>   explicit:   bool
>>>   popularity: int
>>>
>>> @endpoint.GET('get_artists', api, '/artists/top')
>>> class Artist(pyty.Schema):
>>>   id:     int
>>>   name:   str
>>>   genres: List[str]
>>>   tracks: List[Song] = 'alias'   |IS| 'songs' \
>>>                    and 'default' |IS| []
>>>
>>> for artist in Artist.fetch_all():
>>>   for song in artist.songs: # note that JSON key 'tracks' gets renamed as 'songs'
>>>     print(song.name,  song.explicit, song.popularity)
```

## Object Encoding

Schemas can be defined to build objects from raw JSON data. To do so, subclass `pyty.Schema`. Here's a simple example:

```
>>> from pyty import Schema, encode, List
>>>
>>> class User(Schema):
>>>   name: str
>>>   age:  int
>>>
>>> class Group(Schema):
>>>   title:   str
>>>   creator: User
>>>   msg_set: List[str]
>>>
>>> group = encode({
>>>   'title': 'Revolution?',
>>>   'creator': {'name': 'George Washington', 'age': 23},
>>>   'messages': ['When we stealing that tea?', '@theRealKingGeorge 1v1 me irl']
>>> })
>>>
>>> group.title
'Revolution?'
>>> group.creator
<User name='George Washington' age=23>
```

### Constraints

It's possible to allow optional attributes. `REQUIRE_ALL` is turned on by default. To change that:
```
>>> class MyCustomSchema(Schema):
>>>   REQUIRE_ALL = False
```

Then, individual attributes can be `required` like this:
```
>>> class MyCustomSchema(Schema):
>>>   name: id = 'required'
```

Use the `IS` operator to define constraints through a supported keyword and specify a condition.
```
>>> class TRex(Schema):
>>>   armSize: float = 'range' |IS| (0, 0.1)
```

The available keywords are:
- range
- default
- max-size
- min-size
- length

## API Support

### Endpoint Decorator

# TODO
- finish implementing endpoint API stuff
- add support for endpoint decorator on Schema attributes, not just classes.
- add more type checking and make sure all loose ends are tied up
- make it so the Api class can  
- add documentation for the API stuff
- to use `Schema` with the `Api` class and `@endpoint` decorator.
- write some tests
- not really relevant but a private decorator would be awesome if possible
