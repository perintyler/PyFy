# PyObjectValidation

## Installation 

```console
pip install ./PyObjectValidation
```

## Object Encoding

Schemas can be defined to build objects from raw JSON data. To do so, subclass `pyty.Schema`. Here's a simple example:

```console
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
