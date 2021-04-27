import sys
sys.path.append('.')

import unittest
import random
from heaps.rankpairing import RankPairingHeap

n, repeats = 10, 1

class RankPairingTest(unittest.TestCase):
    def setUp(self):
        self.heap = RankPairingHeap()
        self.testcase = [i for i in range(n, -n, -1)]
        random.shuffle(self.testcase)

    def test_insert(self):
        heap = RankPairingHeap() # new heap so that other tests not affected
        for i, element in enumerate(self.testcase, 1):
            heap.insert(element)
            count = heap.count - i

        self.assertEqual(count, 0)
            
    def test_extract(self):
        pops = []
        for element in self.testcase:
            self.heap.insert(element)
        for _ in self.testcase:
            pops.append(self.heap.extract_min().distance)

        self.assertListEqual(pops, sorted(self.testcase))

    def test_extract_repeats(self):
        elements, pops = [i for i in self.testcase for _ in range(repeats)], []
        for element in elements:
            self.heap.insert(element)
        for _ in elements:
            pops.append(self.heap.extract_min().distance)

        self.assertListEqual(pops, sorted(elements))

    def test_merge(self):
        h1, h2 = RankPairingHeap(), RankPairingHeap()
        for i,j in zip(self.testcase[:n], self.testcase[n:]):
            h1.insert(i)
            h2.insert(j)
        h1.merge(h2)

        self.assertTrue(h1.min.distance == min(h1.min.distance, h2.min.distance) and h1.count == 2*n)


def test_extract():
    testcase = [i for i in range(n, -n, -1)]
    heap = RankPairingHeap()
    pops = []
    for i in testcase:
        heap.insert(i)
    for _ in testcase:
        pops.append(heap.extract_min().distance)
    
    print(pops)

def test_decrease_key(elements=None):
    h = RankPairingHeap()
    h.insert(5)
    h.insert(4)
    x = h.insert(100)
    y = h.insert(9)
    h.insert(67)
    h.extract_min()
    h.show(verbose=True)

    h.decrease_key(x, 3) # doesn't work with multiple decrease keys to same value
    h.show(verbose=True)

    # # h.show()
    h.decrease_key(y, 3)
    h.show(verbose=True)
    # assert h.extract_min().distance == 3 # extract x
    # assert y.distance == 1

if __name__ == '__main__':
    # unittest.main()
    test_decrease_key()
    # test_extract()
