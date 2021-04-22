from minheap import MinHeap
from graph import Graph, Vertex


def testGraph():
    g = Graph()
    for i in range(10):
        g.addVertex(Vertex(name=i))
    print(g)
    g.show()


def testHeap(heap=None):
    h = heap or MinHeap()
    V = [Vertex(name=f'v{i}') for i in range(10)]
    for v in V:
        h.insert(v)
    h.show()

    for v in V:
        h.decreaseKey(v, v.distance-10)
        h.show()


def testDijkstra(graph=None, heap=None, show=False):
    h = heap or MinHeap()
    g = graph or Graph()
    for i in range(10):
        g.addVertex(Vertex(name=i))
    for i in range(10):
        g.addEdge(u=i, v=(i+1) % 10, w=2) # make linear cycle graph

    if show:
        g.show()

    g.Dijkstra(1, h)


if __name__ == '__main__':

    # testHeap(HeapqHeap())
    # testHeap()
    testDijkstra(show=False)

    # testGraph()
