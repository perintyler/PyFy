# PyTy

PyTy is a library that provides support for interacting with APIs by offering a quick and easy way to create objects that represent data from an API endpoint. Type safety is a feature and encodable schemas can be defined to validate REST responses.

## Installing


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
