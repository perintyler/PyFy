"""tests.py"""

import pytest

from .schema import Schema, encode, decode, EncodeException

class TestSchema(Schema):
  prop1: str = 'required'
  prop2: int

def test_encoding():
  encoded = encode(TestSchema, {
    'prop1': 'a property',
    'prop2': 2
  })
  assert encoded.prop1 == 'a property'
  assert encoded.prop2 == 2

def test_type_validation():
  with pytest.raises(TypeError):
    encoded = encode(TestSchema, {
      'prop1': 'a property',
      'prop2': 'not an integer'
    })

def test_required_constraint():
  encoded1 = encode(TestSchema, {'prop1': 'a property'})
  assert encoded1.prop1 == 'a property'
  assert encoded1.prop2 is None
  with pytest.raises(EncodeException):
    encoded2 = encode(TestSchema, {
      'prop2': 'missing required prop1',
    })

def test_decode():
  for index in range(1,5):
    decoded = {'prop1': f'property{index}', 'prop2': index}
    encoded = encode(TestSchema, decoded)
    assert decode(encoded) == decoded

