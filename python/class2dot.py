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
  compound=true;
  subgraph isinstance {
    edge [color=red, constraint=false, spline=spline];
'''

        for edge in sorted(self.isinstance):
            result += '    "%s" -> "%s"\n' % (name(edge[1]), name(edge[0]))

        result += '''\
  }
  subgraph issubclass {
'''

        for edge in sorted(self.issubclass):
            result += '    "%s" -> "%s"\n' % (name(edge[1]), name(edge[0]))

        result += '''\
  }
}
'''
        return result


def class2dot(*classes):
    edges = Edges()
    for cls in classes:
        _class2dot(cls, edges=edges)
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
        import_class(classname)
        for classname in argv[1:]
    ))


def import_class(class_string):
    """Return the class object specified by a string.

    Args:
        class_string: The string representing a class.

    Raises:
        ValueError if module part of the class is not specified.
    """
    # From: http://stackoverflow.com/a/3610097/146821
    module_name, _, class_name = class_string.rpartition('.')
    return getattr(
        __import__(module_name, fromlist=["__trash"]),
        class_name,
    )


if __name__ == '__main__':
    exit(main())
