from rankpairingheap import RankPairingHeap


def test_insert(n=5): # WORKS
    h = RankPairingHeap()
    for i in range(n, 0, -1):
        h.insert(i)
    h.show()


def test_merge(n=5): # WORKS
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

def test_delete_min(elements):
    h = RankPairingHeap()
    for element in elements:
        h.insert(element)

    h.show()
    # for _ in elements: # TODO: fix this - the linked list is not collected back
        # h.print_nodes()
        # print(f'Min popped: {h.delete_min()}')
        # h.show(verbose=True)
    # print(h.ranks.items())
    # h.print_nodes()
    for _ in elements:
        print(h.delete_min())




if __name__ == '__main__':
    # test_insert(20)
    # test_merge(10)
    test_delete_min(range(5))
    # test_delete_min(range(-5,0,1))
