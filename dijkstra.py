# import matplotlib.pyplot as plt
# import numpy as np

import sys
sys.path.append('.')
from heap import MinHeap

if __name__ == '__main__':
    h = MinHeap()
    for i in range(10,0,-1):
        h.push(i)
    h.show()

    for i in range(3):
        h.pop()
        h.show()