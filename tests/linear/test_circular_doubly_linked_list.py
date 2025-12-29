import pytest

from core.structures.linear.circular_doubly_linked_list import CircularDoublyLinkedList


def test_push_and_to_list() -> None:
    cdll = CircularDoublyLinkedList[int]()
    cdll.push_back(1)
    cdll.push_back(2)
    cdll.push_front(0)
    assert cdll.to_list() == [0, 1, 2]
    assert len(cdll) == 3


def test_pop_front_back() -> None:
    cdll = CircularDoublyLinkedList[int]()
    for x in [1, 2, 3]:
        cdll.push_back(x)

    assert cdll.pop_front() == 1
    assert cdll.to_list() == [2, 3]

    assert cdll.pop_back() == 3
    assert cdll.to_list() == [2]

    assert cdll.pop_back() == 2
    assert cdll.to_list() == []

    with pytest.raises(IndexError):
        cdll.pop_front()


def test_rotate() -> None:
    cdll = CircularDoublyLinkedList[int]()
    for x in [1, 2, 3, 4]:
        cdll.push_back(x)

    cdll.rotate_left(1)
    assert cdll.to_list() == [2, 3, 4, 1]

    cdll.rotate_right(2)
    assert cdll.to_list() == [4, 1, 2, 3]


def test_delete_and_delete_all() -> None:
    cdll = CircularDoublyLinkedList[int]()
    for x in [1, 2, 2, 3, 2]:
        cdll.push_back(x)

    assert cdll.delete(2) is True
    assert cdll.to_list() == [1, 2, 3, 2]

    assert cdll.delete_all(2) == 2
    assert cdll.to_list() == [1, 3]
    assert len(cdll) == 2
