# -*- coding: utf-8 -*-

"""
pyty.utils
~~~~~~~~~~

This module provides generalized utility used within PyTy.
"""

from functools import partial

def map(f, items):
  return list(map(f, items))

class LinkedListNode:

  def __init__(self):
    self.prev = None
    self.next = None

  def chain(self, node):
    self.next = node
    node.prev = self

class LinkedList(LinkedListNode):

  @property
  def head(self):
    node = self
    while node.prev is not None:
      node = node.prev
    return node

  def __iter__(self):
    node = self.head
    while node:
      yield node
      node = node.next

  def as_list(self):
    return list(iter(self))
