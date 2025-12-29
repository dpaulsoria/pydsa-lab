import pytest

from core.structures.deque_ds import DequeDS


def test_deque_ds_peeks_and_pops() -> None:
    d = DequeDS[int]()
    assert d.peek_front() is None
    assert d.peek_back() is None
    assert d.is_empty() is True
    assert bool(d) is False

    d.push_back(1)
    d.push_front(0)
    d.push_back(2)
    assert d.to_list() == [0, 1, 2]
    assert d.peek_front() == 0
    assert d.peek_back() == 2

    assert d.pop_front() == 0
    assert d.pop_back() == 2
    assert d.to_list() == [1]


def test_deque_ds_pop_empty_raises() -> None:
    d = DequeDS[int]()
    with pytest.raises(IndexError):
        d.pop_front()
    with pytest.raises(IndexError):
        d.pop_back()


def test_deque_ds_clear() -> None:
    d = DequeDS[int]()
    d.push_back(1)
    d.push_back(2)
    d.clear()
    assert d.to_list() == []
    assert d.is_empty() is True
    assert len(d) == 0
