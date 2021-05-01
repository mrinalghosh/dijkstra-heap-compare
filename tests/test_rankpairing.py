""" RankPairing Heap Unit Tests"""

import pytest
from heaps.rankpairing import RankPairingHeap


# Empty RankPairing Heap for test functions
@pytest.fixture
def uut():
    return RankPairingHeap()


def test_insert(uut):
    node = {"key": 5, "value": "apples"}
    test_node = uut.insert(node, node["value"])
    assert test_node.key == 5
    assert test_node.name == "apples"


def test_insert_count(uut):
    uut.insert({"key": 8})
    uut.insert({"key": 7})
    uut.insert({"key": -9})
    uut.insert({"key": 4})
    assert uut.count == 4


def test_find_min(uut):
    uut.insert({"key": 5})
    uut.insert({"key": 4})
    uut.insert({"key": 7})
    uut.insert({"key": 9})
    uut.insert({"key": 67})
    uut.extract_min()  # Extract 4
    uut.extract_min()  # Extract 5
    assert uut.find_min().key == 7


def test_extract_min(uut):
    uut.insert({"key": 5})
    uut.insert({"key": 4})
    uut.insert({"key": 7})
    uut.insert({"key": 9})
    uut.insert({"key": 67})
    assert uut.extract_min().key == 4
    assert uut.extract_min().key == 5


def test_decrease_key(uut):
    uut.insert({"key": 5})
    uut.insert({"key": 4})
    x = uut.insert({"key": 100})
    y = uut.insert({"key": 9})
    uut.insert({"key": 67})
    uut.extract_min()
    uut.decrease_key(x, 3)
    assert uut.extract_min().key == 3  # extract x
    uut.decrease_key(y, 8)
    assert y.key == 8


def test_decrease_key_greater(uut):
    x = uut.insert({"key": 5})
    with pytest.raises(ValueError):
        uut.decrease_key(x, 10)
