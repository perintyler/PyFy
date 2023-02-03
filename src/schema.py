# -*- coding: utf-8 -*-

"""
pyty.schema
~~~~~~~~~~~

This module provides Schema
"""

from typing import List, Dict, TypeVar, Generic, Callable
from abc import ABCMeta as AbstractClass

from .utils import *
from .exceptions import *

CONSTRAINT_KEYWORDS = ['default', 'required', 'range', 'max-size', 'path'
                       'min-size', 'length', 'alias', 'endpoint']

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
      continue
    elif type(data[attrName]) != attrType:
      raise TypeError

    # encode the values of the attributes
    if attrType in (int, float, str, bool):
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
  return map(collapse_object, schema.attributes().values())

class Attribute:

  def __init__(self, name, value):
    self.name = name
    self.value = value
    self.constraints = {}

  def add_constraint(self, constraint):
    if not constraint.validate():
      raise ConstraintException('Invalid Constraint')
    self.constraints[constraint.keyword] = constraint

  def is_optional():
    return 'required' in self.constraint.keys()

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

class Constraint:

  KEYWORDS = ['default', 'required', 'range', 'max-size', 'path'
              'min-size', 'length', 'alias', 'endpoint']

  def __init__(self, keyword: str, condition: any):
    if keyword not in CONSTRAINT_KEYWORDS:
      print(keyword, condition)
      raise ConstraintException()
    self.keyword = keyword
    self.condition = condition

  def __repr__(self):
    return f'<Constraints keyword={self.keyword} condition={self.condition}>'

class ConstraintChain(Constraint, LinkedList):

  def __and__(self, other):
    if not isinstance(other, ConstraintChain):
      raise ConstraintException()
    self.chain(other)

class ConstraintBuilder(object):
  """Constraint Operator Decoration

  I can't believe this works... Usage:
  >>> @ConstraintSymbol
  >>> def EQUAL(a, b) -> Constraint:
  >>>   return a == b
  >>> print(2 |EQUAL| 3) # False
  """

  def __init__(self, operator: Callable):
    self.operator = operator

  def __or__(self, condition):
    # TODO: figure out best way to validate that the condition type fits the keyword
    return self.operator(condition)

  def __ror__(self, keyword):
    if not isinstance(keyword, str) or keyword not in Constraint.KEYWORDS:
      raise ConstraintOperator('Invalid left side')
    partialFunc = partial(self.operator, keyword)
    return ConstraintBuilder(partialFunc)

  def __call__(self, keyword, condition):
    return self.operator(keyword, condition)

@ConstraintBuilder
class IS:
  """Special operator used to define constraints"""
  def __call__(keyword, condition):
    return ConstraintChain(keyword, condition)
