import sys
sys.path.append('.')

import unittest
import random
from heaps.rankpairing import RankPairingHeap

n, repeats = 10000, 3

class RankPairingTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)

    def test_extract(self, elements=None):
        elements = elements or [i for i in range(n, -n, -1)]
        random.shuffle(elements)
        h = RankPairingHeap()
        pops = []

        for element in elements:
            h.insert(element)

        for _ in elements:
            pops.append(h.extract_min())

        self.assertListEqual(pops, sorted(elements))

    def test_extract_repeats(self, elements=None):
        elements = elements or [i for i in range(n, -n, -1) for _ in range(repeats)]
        random.shuffle(elements)
        h = RankPairingHeap()
        pops = []

        for element in elements:
            h.insert(element)

        for _ in elements:
            pops.append(h.extract_min())

        self.assertListEqual(pops, sorted(elements))

def test_insert(n=5):
    h = RankPairingHeap()
    for i in range(n, 0, -1):
        h.insert(i)
    h.show()


def test_merge(n=5):
    h1, h2 = RankPairingHeap(), RankPairingHeap()

    for i in range(n, 0, -1):  # insert reverse magnitude
        h1.insert(i)
        h2.insert(i+n)

    h1.show()
    h2.show()

    h2.merge(h1)
    h2.show()


def test_decrease_key(elements=None):
    random.shuffle(elements)
    h = RankPairingHeap()
    pops = []

    for element in elements:
        h.insert(element)

    diff = sum(i != j for i, j in zip(pops, sorted(elements)))

    if diff == 0:
        print('(decrease_key) PASSED - all decrease_key in correct order')
    else:
        print(f'(decrease_key) FAILED - {diff} decrease_key were wrong')


if __name__ == '__main__':
    # test_merge()
    # test_extract_min()
    unittest.main()
