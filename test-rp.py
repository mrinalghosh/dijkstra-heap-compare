from rankpairingheap import RankPairingHeap


def test_insert(n=5):
    h = RankPairingHeap()
    for i in range(n, 0, -1):
        h.insert(i)
    h.show()


def test_merge(n=5):
    h1, h2 = RankPairingHeap(), RankPairingHeap()
    # for i in range(n):
    for i in range(n, 0, -1):  # insert reverse magnitude
        h1.insert(i)
        h2.insert(i+n)

    h1.show()
    h2.show()

    # h1.merge(h2)
    # h1.show()

    h2.merge(h1)
    h2.show()

def test_compress(n=5):
    h = RankPairingHeap()
    for i in range(n):
        h.insert(i)
    h.compress()
    print(h.ranks.items())


if __name__ == '__main__':
    # test_insert(20)
    # test_merge(10)
    test_compress()
