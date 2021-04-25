import pytest
from heaps import quakeheap as quake

# Set up an empty Quake heap for test functions
@pytest.fixture
def uut():
    return quake.QuakeHeap()

def test__find_min_node(uut):
    uut.insert(8)
    uut.insert(7)
    uut.insert(-9)
    uut.insert(4)
    assert uut._find_min_node().key == -9