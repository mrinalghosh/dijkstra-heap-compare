from heaps.rankpairing import RankPairingHeap
import random
import unittest

n, repeats = 1000, 3
testcase = [i for i in range(n) for _ in range(repeats)]

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


def test_delete_min(elements=testcase):
    random.shuffle(elements)
    h = RankPairingHeap()
    pops = []

    for element in elements:
        h.insert(element)

    for _ in elements:
        pops.append(h.delete_min())

    diff = sum(i != j for i, j in zip(pops, sorted(elements)))

    if diff == 0:
        print('(delete_min) PASSED - all delete_min in correct order')
    else:
        print(f'(delete_min) FAILED - {diff} delete_min were wrong')

def test_decrease_key(elements=testcase):
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
    test_delete_min()

