import pytest

from core.structures.queue import Queue


def test_queue_enqueue_dequeue_fifo() -> None:
    q = Queue[int]()
    q.enqueue(8)
    q.enqueue(3)
    q.enqueue(2)

    assert q.to_list() == [8, 3, 2]
    assert len(q) == 3

    assert q.dequeue() == 8
    assert q.dequeue() == 3
    assert q.dequeue() == 2
    assert q.to_list() == []
    assert len(q) == 0


def test_queue_front_does_not_remove() -> None:
    q = Queue[int]()
    assert q.front() is None

    q.enqueue(10)
    q.enqueue(20)

    assert q.front() == 10
    assert q.to_list() == [10, 20]
    assert len(q) == 2


def test_queue_dequeue_empty_raises() -> None:
    q = Queue[int]()
    with pytest.raises(IndexError):
        q.dequeue()


def test_queue_bool_is_empty_clear() -> None:
    q = Queue[int]()
    assert bool(q) is False
    assert q.is_empty() is True

    q.enqueue(1)
    assert bool(q) is True
    assert q.is_empty() is False

    q.clear()
    assert q.to_list() == []
    assert len(q) == 0
    assert q.is_empty() is True
