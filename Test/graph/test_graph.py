import pytest
import config
from DISClib.DataStructures import edge as e
from DISClib.ADT import graph as g
assert config


@pytest.fixture
def graph():
    graph = g.newGraph(size=10, comparefunction=comparenames)
    return graph


@pytest.fixture
def digraph():
    digraph = g.newGraph(size=10, directed=True,
                         comparefunction=comparenames)
    return digraph


def test_edgeMethods(graph):
    edge = e.newEdge('Bogota', 'Cali')
    assert 'Bogota' == e.either(edge)
    assert 'Cali' == e.other(edge, e.either(edge))
    assert e.weight(edge) == 0


def test_insertVertex(graph):
    g.insertVertex(graph, 'Bogota')
    g.insertVertex(graph, 'Yopal')
    g.insertVertex(graph, 'Cali')
    g.insertVertex(graph, 'Medellin')
    g.insertVertex(graph, 'Pasto')
    g.insertVertex(graph, 'Barranquilla')
    g.insertVertex(graph, 'Manizales')
    assert g.numVertex(graph) == 7


def test_insertEdges(graph):
    g.insertVertex(graph, 'Bogota')
    g.insertVertex(graph, 'Yopal')
    g.insertVertex(graph, 'Cali')
    g.insertVertex(graph, 'Medellin')
    g.insertVertex(graph, 'Pasto')
    g.insertVertex(graph, 'Barranquilla')
    g.insertVertex(graph, 'Manizales')
    g.addEdge(graph, 'Bogota', 'Yopal')
    g.addEdge(graph, 'Bogota', 'Medellin')
    g.addEdge(graph, 'Bogota', 'Pasto')
    g.addEdge(graph, 'Bogota', 'Cali')
    g.addEdge(graph, 'Yopal', 'Medellin')
    g.addEdge(graph, 'Medellin', 'Pasto')
    g.addEdge(graph, 'Cali', 'Pasto')
    g.addEdge(graph, 'Cali', 'Barranquilla')
    g.addEdge(graph, 'Barranquilla', 'Manizales')
    g.addEdge(graph, 'Pasto', 'Manizales')
    assert g.numVertex(graph) == 7
    assert g.numEdges(graph) == 10


def comparenames(searchname, element):
    if (searchname == element['key']):
        return 0
    elif (searchname < element['key']):
        return -1
    return 1


def comparelst(self, searchname, element):
    return (searchname == element)


def test_newEdge():
    edge = e.newEdge(1, 1, 1)
    assert edge is not None