import sys
sys.path.append("..")
import pytest
from heaps import quakeheap
from heaps.quakeheap import Vertex

v8 = Vertex(8)
v1 = Vertex(1)
v2 = Vertex(2)
v3 = Vertex(3)
v4 = Vertex(4)
v5 = Vertex(5)
v6 = Vertex(6)
v7 = Vertex(7)
# Set up an empty Fibonacci heap for test functions
@pytest.fixture
def uut():
 
    return quakeheap.QuakeHeap()

# Set up an empty Quake heap for test functions
def test_insert(uut):
    uut.insert(v1)
    uut.insert(v2)
    uut.insert(v3)
    uut.insert(v4)
    uut.insert(v5)
    uut.insert(v6)
    uut.insert(v7)
    uut.insert(v8) 
    assert uut.peak_min().key == 1


def test__extract_min(uut):
    uut.insert(v1)
    uut.insert(v2)
    uut.insert(v3)
    uut.insert(v4)
    uut.insert(v5)
    uut.insert(v6)
    uut.insert(v7)
    uut.insert(v8) 
    assert uut.extract_min().key == 1


def test_decrease_key(uut):
    v8 = Vertex(18)
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)
    v4 = Vertex(4)
    v5 = Vertex(5)
    v6 = Vertex(6)
    v7 = Vertex(7)
    uut.insert(v1)
    uut.insert(v2)
    uut.insert(v3)
    uut.insert(v4)
    uut.insert(v5)
    uut.insert(v6)
    uut.insert(v7)
    uut.insert(v8) 
    uut.extract_min()
    uut.decrease_key(v7, 0)
    assert uut.extract_min().key == 0
    uut.decrease_key(v8, 8)
    assert v8.key == 8