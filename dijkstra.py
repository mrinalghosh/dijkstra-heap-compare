# import matplotlib.pyplot as plt
# import numpy as np
import sys
sys.path.append('.')
from heap import *

if __name__ == '__main__':
    h = MinHeap()
    # h = HeapqHeap()
    for i in range(10,0,-1):
        h.push(Vertex(i))
    # h.show()

    for i in range(3):
        h.pop()
    h.show()