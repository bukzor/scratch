# Albert ten Napel:  12:48 AM
# How I see it: a type parameter cannot affect which constructors you may find
# for a type. For example a List T will be either Nil or Cons for any choice of
# T. But an index can change what constructors you may find. For example a
# Vector Z will never be Cons and a Vector (S n) will never be Nil.
from dataclass import dataclass
from typing import TypeVar

T = TypeVar('T')      # Declare type variable



@dataclass
class List:
    this: T
    next: List(T)

    nil = 

    def nil(self):

