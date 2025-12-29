import pytest

from core.structures.linear.linked_list import LinkedList


def test_linked_list_push_front_and_append() -> None:
    ll = LinkedList[int]()
    ll.push_front(2)  # [2]
    ll.push_front(3)  # [3,2]
    ll.append(9)  # [3,2,9]

    assert ll.to_list() == [3, 2, 9]
    assert len(ll) == 3


def test_linked_list_find_index() -> None:
    ll = LinkedList[int]()
    for x in [5, 7, 9]:
        ll.append(x)

    assert ll.find_index(5) == 0
    assert ll.find_index(7) == 1
    assert ll.find_index(9) == 2
    assert ll.find_index(100) is None


def test_linked_list_delete_first_occurrence() -> None:
    ll = LinkedList[int]()
    for x in [1, 1, 2, 1]:
        ll.append(x)

    assert ll.to_list() == [1, 1, 2, 1]
    assert len(ll) == 4

    assert ll.delete(1) is True
    assert ll.to_list() == [1, 2, 1]
    assert len(ll) == 3

    assert ll.delete(99) is False
    assert ll.to_list() == [1, 2, 1]
    assert len(ll) == 3


def test_linked_list_delete_all() -> None:
    ll = LinkedList[int]()
    for x in [1, 1, 2, 1, 3, 1]:
        ll.append(x)

    assert len(ll) == 6
    removed = ll.delete_all(1)

    assert removed == 4
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2


def test_linked_list_delete_at() -> None:
    ll = LinkedList[int]()
    for x in [10, 20, 30, 40]:
        ll.append(x)

    assert ll.to_list() == [10, 20, 30, 40]
    assert ll.delete_at(0) == 10
    assert ll.to_list() == [20, 30, 40]
    assert len(ll) == 3

    assert ll.delete_at(1) == 30
    assert ll.to_list() == [20, 40]
    assert len(ll) == 2

    with pytest.raises(IndexError):
        ll.delete_at(-1)

    with pytest.raises(IndexError):
        ll.delete_at(999)


def test_linked_list_delete_at_empty_raises() -> None:
    ll = LinkedList[int]()
    with pytest.raises(IndexError):
        ll.delete_at(0)
