# PyTy

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

I think this would be cool. 

```
>>> from pyty import Schema, Api, IS, List
>>>
>>> api = pyty.Api('<API-URI>')
>>> api.request_token('<CLIENT-ID>', '<SECRET-KEY>', authUrl = AUTH_URL)
>>>
>>> class Songs(pyty.Schema):
>>>   name:       str
>>>   popularity: int
>>>
>>> @endpoint.GET('get_top_artists', api, '/artists/top')
>>> class Artist(pyty.Schema):
>>>   name:   str
>>>   genres: List[str]
>>>   tracks: List[Song] = 'alias'   |IS| 'songs' \
>>>                    and 'default' |IS| []
>>>
>>> for artist in Artist.get_top_artists(): # func name get_top_artists set in endpoint decorator
>>>   for song in artist.songs: # note that JSON key 'tracks' gets renamed as 'songs'
>>>     print(song.name,  song.explicit, song.popularity)
```


