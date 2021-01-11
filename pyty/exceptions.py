# -*- coding: utf-8 -*-

"""
pyty.exceptions
~~~~~~~~~~~~~~~

This module contains the set of PyTy's exceptions.
"""

class EncodeException(Exception):
    """Schema does not match the data"""

class ConstraintException(Exception):
    """A schema contains an invalid constraint"""

class ApiException(Exception):
    """A bad API response was recieved or auth was done wrong"""
