import sys
sys.path.append('.')

import pytest
from heaps.rankpairing import RankPairingHeap


@pytest.fixture
def uut():
    return RankPairingHeap()


def test_insert(uut):
    test_node = uut.insert(5)
    assert test_node.distance == 5


def test_find_min(uut):
    uut.insert(8)
    uut.insert(7)
    uut.insert(-9)
    uut.insert(4)
    assert uut.find_min().distance == -9


def test_find_min(uut):
    uut.insert(5)
    uut.insert(4)
    uut.insert(7)
    uut.insert(9)
    uut.insert(67)
    uut.extract_min()  # Extract 4
    uut.extract_min()  # Extract 5
    assert uut.find_min().distance == 7


def test_extract_min(uut):
    uut.insert(5)
    uut.insert(4)
    uut.insert(7)
    uut.insert(9)
    uut.insert(67)
    assert uut.extract_min().distance == 4
    assert uut.extract_min().distance == 5


def test_decrease_key(uut):
    uut.insert(5)
    uut.insert(4)
    x = uut.insert(100)
    y = uut.insert(9)
    uut.insert(67)
    uut.extract_min()
    uut.decrease_key(x, 3)
    assert uut.extract_min().distance == 3  # extract x
    uut.decrease_key(y, 8)
    assert y.distance == 8


def test_decrease_key_greater(uut):
    x = uut.insert(5)
    with pytest.raises(ValueError):
        uut.decrease_key(x, 10)
