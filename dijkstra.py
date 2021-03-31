# import matplotlib.pyplot as plt
# import numpy as np
import sys
sys.path.append('.')
from heap import *

if __name__ == '__main__':
    # # h = MinHeap()
    # h = HeapqHeap()
    # for i in range(10,0,-1):
    #     h.push(Vertex(i))
    # for i in range(3):
    #     h.pop()
    # h.show()

    g = Graph()

    for i in range(100):
        g.addVertex(Vertex(i, id=f'n-{i}'))
    
    print(g)
    g.show()