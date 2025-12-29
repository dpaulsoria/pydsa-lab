import pytest

from core.structures.linear.array_list import ArrayList


def test_array_list_basic() -> None:
    a = ArrayList[int]()
    a.append(1)
    a.append(2)
    a.insert(1, 9)
    assert a.to_list() == [1, 9, 2]
    assert a.get(0) == 1
    a.set(0, 7)
    assert a.to_list() == [7, 9, 2]
    assert a.remove_first(9) is True
    assert a.to_list() == [7, 2]
    assert a.pop() == 2
    assert a.to_list() == [7]
    a.clear()
    assert a.to_list() == []
    with pytest.raises(IndexError):
        a.pop()
