"""
python class2dot.py | dot -Tsvg | ssh people 'cat > public_html/class2dot/type.svg'
"""
#pylint:disable=missing-docstring, too-few-public-methods
class DotGraph(object):
    styles = ()
    components = set()


class Edges(object):
    def __init__(self):
        self.isinstance = set()
        self.issubclass = set()

    def __str__(self):
        result = '''\
digraph G {
  splines=true;
  sep="+25,25";
  overlap=scalexy;
  nodesep=0.6;
  node [shape=plaintext, fontsize=11];
  compound=true;
  subgraph isinstance {
    edge [color=red, constraint=false, spline=spline];
'''

        for edge in sorted(self.isinstance):
            result += '    "%s" -> "%s"\n' % (name(edge[0]), name(edge[1]))

        result += '''\
  }
  subgraph issubclass {
'''

        for edge in sorted(self.issubclass):
            result += '    "%s" -> "%s"\n' % (name(edge[0]), name(edge[1]))

        result += '''\
  }
}
'''
        return result


def class2dot(*objects):
    import inspect
    edges = Edges()
    for obj in objects:
        if inspect.ismodule(obj):
            module = obj
            for obj in vars(module).values():
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    _class2dot(obj, edges=edges)
        elif inspect.isclass(obj):
            _class2dot(obj, edges=edges)
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


def test():
    type_edges = class2dot(type)
    object_edges = class2dot(object)

    assert type_edges.isinstance == object_edges.isinstance
    assert type_edges.issubclass == object_edges.issubclass
    print 'OK'


def main():
    from sys import argv
    print class2dot(*tuple(
        import_object(objname)
        for objname in argv[1:]
    ))


def import_object(dotted_path):
    """Return the object specified by a string.

    Args:
        dotted_path: The string naming an object.

    Raises:
        ValueError if module part of the class is not specified.
    """
    module_name, dot, object_name = dotted_path.rpartition('.')

    if dot:
        return getattr(
            __import__(module_name, fromlist=["__trash"]),
            object_name,
        )
    else:
        # They asked for a top-level module
        return __import__(object_name, fromlist=["__trash"])


if __name__ == '__main__':
    exit(main())
