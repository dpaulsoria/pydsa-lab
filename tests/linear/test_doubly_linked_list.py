import pytest

from core.algos.linear.doubly_linked_list_ops import build_steps, parse_operations
from core.render.linear.doubly_linked_list_graphviz import doubly_linked_list_to_dot
from core.structures.linear.doubly_linked_list import DoublyLinkedList


def test_push_front_push_back_and_reverse() -> None:
    dll = DoublyLinkedList[int]()
    dll.push_back(2)
    dll.push_back(3)
    dll.push_front(1)

    assert dll.to_list() == [1, 2, 3]
    assert dll.to_reverse_list() == [3, 2, 1]
    assert len(dll) == 3


def test_pop_front_pop_back() -> None:
    dll = DoublyLinkedList[int]()
    for x in [1, 2, 3]:
        dll.push_back(x)

    assert dll.pop_front() == 1
    assert dll.to_list() == [2, 3]
    assert len(dll) == 2

    assert dll.pop_back() == 3
    assert dll.to_list() == [2]
    assert dll.to_reverse_list() == [2]
    assert len(dll) == 1

    assert dll.pop_back() == 2
    assert dll.to_list() == []
    assert len(dll) == 0

    with pytest.raises(IndexError):
        dll.pop_front()


def test_delete_first_occurrence() -> None:
    dll = DoublyLinkedList[int]()
    for x in [1, 1, 2, 1]:
        dll.push_back(x)

    assert dll.delete(1) is True
    assert dll.to_list() == [1, 2, 1]
    assert len(dll) == 3

    assert dll.delete(99) is False
    assert dll.to_list() == [1, 2, 1]
    assert len(dll) == 3


def test_delete_all() -> None:
    dll = DoublyLinkedList[int]()
    for x in [1, 1, 2, 1, 3, 1]:
        dll.push_back(x)

    removed = dll.delete_all(1)
    assert removed == 4
    assert dll.to_list() == [2, 3]
    assert dll.to_reverse_list() == [3, 2]
    assert len(dll) == 2


def test_delete_at() -> None:
    dll = DoublyLinkedList[int]()
    for x in [10, 20, 30, 40]:
        dll.push_back(x)

    assert dll.delete_at(0) == 10
    assert dll.to_list() == [20, 30, 40]
    assert len(dll) == 3

    assert dll.delete_at(1) == 30
    assert dll.to_list() == [20, 40]
    assert dll.to_reverse_list() == [40, 20]
    assert len(dll) == 2

    with pytest.raises(IndexError):
        dll.delete_at(-1)

    with pytest.raises(IndexError):
        dll.delete_at(999)


def test_dll_ops_basic() -> None:
    ops = parse_operations("push_back 1\npush_back 2\nreverse\n")
    steps = build_steps(ops, dot_builder=doubly_linked_list_to_dot)
    assert steps[-1].values == [2, 1]
    assert "digraph" in steps[-1].dot


def test_dll_empty_and_singleton_cases() -> None:
    dll = DoublyLinkedList[int]()
    assert dll.to_list() == []
    assert dll.to_reverse_list() == []
    dll.reverse()
    assert dll.to_list() == []

    dll.push_back(1)
    assert dll.to_list() == [1]
    assert dll.to_reverse_list() == [1]
    dll.reverse()
    assert dll.to_list() == [1]


def test_dll_pop_back_empty_raises() -> None:
    dll = DoublyLinkedList[int]()
    with pytest.raises(IndexError):
        dll.pop_back()


def test_dll_delete_at_out_of_range() -> None:
    dll = DoublyLinkedList[int]()
    dll.push_back(1)
    with pytest.raises(IndexError):
        dll.delete_at(1)
