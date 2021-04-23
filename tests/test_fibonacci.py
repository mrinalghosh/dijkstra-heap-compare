import pytest
from heaps import fibonacci

# Set up an empty Fibonacci heap for test functions
@pytest.fixture
def uut():
    return fibonacci.FibHeap()


def test_insert(uut):
    test_node = uut.insert(5, "apples")
    assert test_node.key == 5
    assert test_node.value == "apples"


def test_find_min_node(uut):
    uut.insert(8)
    uut.insert(7)
    uut.insert(-9)
    uut.insert(4)
    assert uut.find_min_node().key == -9


def test_find_min(uut):
    uut.insert(5)
    uut.insert(4)
    uut.insert(7)
    uut.insert(9)
    uut.insert(67)
    uut.extract_min()  # Extract 4
    uut.extract_min()  # Extract 5
    assert uut.find_min_node().key == 7


def test_extract_min(uut):
    uut.insert(5)
    uut.insert(4)
    uut.insert(7)
    uut.insert(9)
    uut.insert(67)
    assert uut.extract_min().key == 4
    assert uut.extract_min().key == 5


def test_decrease_key(uut):
    uut.insert(5)
    uut.insert(4)
    x = uut.insert(100)
    y = uut.insert(9)
    uut.insert(67)
    uut.extract_min()
    uut.decrease_key(x, 3)
    assert uut.extract_min().key == 3  # extract x
    uut.decrease_key(y, 8)
    assert y.key == 8


def test_decrease_key_greater(uut):
    x = uut.insert(5)
    with pytest.raises(ValueError):
        uut.decrease_key(x, 10)
