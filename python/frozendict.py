from collections import Mapping

class FrozenDict(Mapping):
    """An immutable dict-like object"""
    __slots__ = ('__d', '__hash')
    __d = None
    __hash = None
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls) # super() is useless here. Sigh.
        object.__setattr__(self, '_FrozenDict__d', dict(*args, **kwargs))
        return self

    def __iter__(self):
        return iter(self.__d)

    def __len__(self):
        return len(self.__d)

    def __getitem__(self, key):
        return self.__d[key]

    def __hash__(self):
        result = self.__hash
        if result is None:
            # it's necessary to sort the items here to get a repeatable hash.
            # We can cache the result to keep the cost down, since the values won't be changing.
            result = hash(tuple(sorted(self.__d.items())))
            object.__setattr__(self, '_FrozenDict__hash', result)
        return result

    def copy(self):
        # An immutable copy is cheap.
        return self

    def update(self, *dicts, **kwargs):
        """Similar to dict.update, but returns a new object (since frozendict is immutable)."""
        cls = type(self)
        all_items = self.items()
        all_items += tuple(
                item
                for d in dicts
                for item in (
                    d.items() if isinstance(d, Mapping) else d
                )
        )
        all_items += kwargs.items()
        return cls(all_items)


    # Be immutable: we have no attributes.
    # This gives identical behavior to setattr/delattr/.__dict__ on a plain-old dict.
    def __noattr(self, attr='__dict__', value=None):
        clsname = type(self).__name__
        raise AttributeError("{clsname!r} object has no attribute {attr!r}".format(
            clsname=clsname, attr=attr,
        ))
    __setattr__ = __delattr__ = __noattr
    __dict__ = property(__noattr)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.__d)
