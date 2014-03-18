"""
python class2dot.py | dot -Tsvg | ssh people 'cat > public_html/class2dot/type.svg'
"""
#pylint:disable=missing-docstring, too-few-public-methods
class DotGraph(object):
    styles = ()
    components = set()


def Edges():
    class Edges(object):
        isinstance = set()
        issubclass = set()
    return Edges


def class2dot(cls):
    edges = _class2dot(cls, edges=Edges())

    print '''\
digraph G {
  compound=true;
  subgraph isinstance {'''

    for edge in edges.isinstance:
        print '    "%s" -> "%s"' % (name(edge[1]), name(edge[0]))

    print '''\
  }
  subgraph issubclass {
    edge [color=red, constraint=false];'''

    for edge in edges.issubclass:
        print '    "%s" -> "%s"' % (name(edge[1]), name(edge[0]))

    print '''\
  }
}'''

    return edges


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

    return '.'.join(parts)


def main():
    type_edges = class2dot(type)
    return

    object_edges = class2dot(object)

    assert type_edges.isinstance == object_edges.isinstance
    assert type_edges.issubclass == object_edges.issubclass
    print 'OK'

if __name__ == '__main__':
    exit(main())
