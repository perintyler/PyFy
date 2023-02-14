"""
  PyObjectValidation.schema
  ~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides Schema
"""

from typing import List, Dict, TypeVar, Generic, Callable
from abc import ABCMeta as AbstractClass

from .exceptions import EncodeException

class EncodeException(Exception):
    """Schema does not match the data"""

def encode(cls, data):
  """Build Object

  A `Schema` object takes advantage of Python's Type Hint support. Type Hints,
  also called annotations, are treated as Type Rules for a `Schema`. Unlike
  with Type Hints, Type Rules are actually enforced to achieve type safety.
  Type Hints: https://docs.python.org/3/library/typing.html

  Parameters:
    cls(Type[Schema]): the `Schema` type to instantiate and build
    data(dict): the raw data to encode

  Returns:
    schema(Schema): the built Schema object from the encoded data
  """
  schema = cls()

  typeRules = schema.__annotations__.items()
  for attrName, attrType in typeRules:
    required = cls.__dict__.get(attrName, '') == 'required' or not cls.OPTIONAL

    # validate data before trying to encode
    if required and attrName not in data:
      raise EncodeException(f'{attrName} not in data')
    elif attrName not in data or data[attrName] is None:
      attribute = None
    elif type(data[attrName]) != attrType:
      raise TypeError
    # encode the values of the attributes
    elif attrType in (int, float, str, bool):
      attribute = attrType(data[attrName])
    elif attrType is list:
      attribute = [encode(type(el), el) for el in data[attrName]]
    else:
      # nested object
      attribute = encode(attrType, data[attrName])

    # define the schema instance's attribute
    setattr(schema, attrName, attribute)

  return schema

def decode(schema):
  """Collapse Object

  Parameters:
    schema(Schema): and instance of a Schema to convert to raw data

  Returns:
    data(dict): the (nested) dictionary made up of all the attributes of
    the Schema instance provided as a paramater
  """
  if type(schema) in (int, float, bool, str, list):
    return schema
  else:
    return {name: decode(value) for name, value in schema.attributes().items()}

class Schema(metaclass=AbstractClass):
  """Schema support for attributes, types, and constraints"""

  # TODO: Implement these
  STRICT      = False
  GREEDY      = False
  OPTIONAL    = True
  REQUIRE_ALL = False

  @classmethod
  def __subclasshook__(cls, subclass):
    return hasattr(cls, '__annotations__')

  def attributes_names(self):
    return self.__dict__.keys()

  def type_rules(self):
    return self.__annotations__.items()

  def attributes(self):
    return self.__dict__
