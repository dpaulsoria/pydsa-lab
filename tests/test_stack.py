import pytest

from core.structures.stack import Stack


def test_stack_push_pop_lifo() -> None:
    s = Stack[int]()

    s.push(8)
    s.push(3)
    s.push(2)

    assert s.to_list() == [8, 3, 2]
    assert len(s) == 3

    assert s.pop() == 2
    assert s.pop() == 3
    assert s.pop() == 8
    assert s.to_list() == []
    assert len(s) == 0


def test_stack_peek_does_not_remove() -> None:
    s = Stack[int]()
    assert s.peek() is None

    s.push(10)
    s.push(20)

    assert s.peek() == 20
    assert s.to_list() == [10, 20]
    assert len(s) == 2


def test_stack_pop_empty_raises() -> None:
    s = Stack[int]()
    with pytest.raises(IndexError):
        s.pop()


def test_stack_bool_is_empty_clear() -> None:
    s = Stack[int]()
    assert bool(s) is False
    assert s.is_empty() is True

    s.push(1)
    assert bool(s) is True
    assert s.is_empty() is False

    s.clear()
    assert s.to_list() == []
    assert len(s) == 0
    assert s.is_empty() is True
