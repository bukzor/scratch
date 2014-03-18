#pylint:disable=missing-docstring, too-few-public-methods
class DotGraph(object):
    styles = ()
    components = set()


def class2dot(cls):
    class Edges(object):
        isinstance = set()
        issubclass = set()

    return _class2dot(cls, edges=Edges)


def _class2dot(cls, edges):
    mcs = type(cls)
    edge = (cls, mcs)
    if edge not in edges.isinstance:
        edges.isinstance.add(edge)
        _class2dot(mcs, edges)

    for base in cls.__bases__:
        edge = (cls, base)
        if edge not in edges.issubclass:
            edges.issubclass.add(edge)
            _class2dot(base, edges)

    return edges


def name(obj):
    parts = []
    if hasattr(obj, '__module__'):
        parts.append(obj.__module__)
    if hasattr(obj, '__name__'):
        parts.append(obj.__name__)
    else:
        raise NotImplementedError(repr(obj))


def main():
    type_edges = class2dot(type)
    object_edges = class2dot(object)

    assert type_edges.isinstance == object_edges.isinstance
    assert type_edges.issubclass == object_edges.issubclass
    print 'OK'

if __name__ == '__main__':
    exit(main())
