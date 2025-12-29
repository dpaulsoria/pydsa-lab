import pytest

from core.structures.ring_buffer import RingBuffer


def test_basic_write_read_wrap() -> None:
    rb = RingBuffer[int](capacity=3)
    rb.write(1)
    rb.write(2)
    rb.write(3)
    assert rb.to_list() == [1, 2, 3]
    assert rb.read() == 1
    rb.write(4)  # wrap
    assert rb.to_list() == [2, 3, 4]


def test_overflow() -> None:
    rb = RingBuffer[int](capacity=2)
    rb.write(1)
    rb.write(2)
    with pytest.raises(OverflowError):
        rb.write(3)


def test_write_over() -> None:
    rb = RingBuffer[int](capacity=3)
    rb.write(1)
    rb.write(2)
    rb.write(3)
    rb.write_over(9)
    assert rb.to_list() == [2, 3, 9]
    assert len(rb) == 3


def test_peek_clear() -> None:
    rb = RingBuffer[int](capacity=2)
    assert rb.peek() is None
    rb.write(7)
    assert rb.peek() == 7
    rb.clear()
    assert rb.peek() is None
    assert rb.to_list() == []
