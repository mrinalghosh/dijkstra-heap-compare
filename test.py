from heap import *


def testGraph():
    g = Graph()
    for i in range(100):
        g.addVertex(Vertex(name=i, dist=100-i))
    print(g)
    g.show()


def testHeap(heap=None):
    h = heap or MinHeap()
    V = [Vertex(name=i, dist=10-i) for i in range(10)]
    for v in V:
        h.push(v)
    h.show()

    for v in V:
        h.decreaseKey(v, v.dist-10)
        h.show()


def testDijkstra(graph=None, heap=None, show=False):
    h = heap or MinHeap()
    g = graph or Graph()
    for i in range(100):
        g.addVertex(Vertex(name=i, dist=i))
    for i in range(100):
        g.addEdge(u=i, v=(i+1) % 100, w=2)

    if show:
        g.show()

    g.Dijkstra(1, h)


if __name__ == '__main__':

    # testHeap(HeapqHeap())
    testHeap()
    # testDijkstra(show=True)

    # testGraph()
