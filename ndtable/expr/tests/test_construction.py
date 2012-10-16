from ndtable.expr.viz import dump
from ndtable.expr.nodes import Node, traverse
from ndtable.expr.graph import NDTable, ScalarNode

DEBUG = False

def test_walk():
    e = Node([])
    d = Node([])
    b = Node([d])
    c = Node([e])
    a = Node([b,c])

    assert len([n for n in a]) == 4

    #if DEBUG:
    dump(a, filename='walk', tree=True)

def test_traverse():
    e = Node([])
    d = Node([])
    b = Node([d])
    c = Node([e])
    a = Node([b,c])

    [n for n in traverse(a)]

    #if DEBUG:
    dump(a, filename='walk', tree=True)

def test_scalar_arguments():
    a = NDTable([1,2,3])
    children = a.children

    assert len(children) == 3

def test_dynamic_arguments():
    a = NDTable([])
    b = NDTable([a])

    children = b.children
    assert len(children) == 1

def test_dynamic_explicit():
    a = NDTable([])
    b = NDTable([a], depends=[a])

    children = b.children
    assert len(children) == 1

def test_binary_ops():
    a = NDTable([])
    b = NDTable([])

    x = a+b
    y = x*a

    #if DEBUG:
    dump(y, filename='binary')

def test_unary_ops():
    a = NDTable([])

    x = abs(a)

    #if DEBUG:
    dump(x, filename='unary')

def test_indexing():
    a = NDTable([])

    x = a[0]

    #if DEBUG:
    dump(x, filename='indexer')

def test_slice():
    a = NDTable([])

    x = a[0:1]

    #if DEBUG:
    dump(x, filename='indexer')

def test_scalars():
    a = ScalarNode(1)
    b = ScalarNode(1)

    x = NDTable([a,b])

    #if DEBUG:
    dump(x, filename='scalars')
