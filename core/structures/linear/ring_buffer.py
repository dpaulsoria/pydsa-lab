from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class RingBuffer(Generic[T]):
    _buf: list[T | None]
    _head: int
    _tail: int
    _size: int

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._buf = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def capacity(self) -> int:
        return len(self._buf)

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self.capacity()

    def clear(self) -> None:
        self._buf = [None] * self.capacity()
        self._head = self._tail = self._size = 0

    def peek(self) -> T | None:
        if self._size == 0:
            return None
        v = self._buf[self._head]
        assert v is not None
        return v

    def write(self, value: T) -> None:
        """Enqueue (sin overwrite)."""
        if self.is_full():
            raise OverflowError("write into full RingBuffer")
        self._buf[self._tail] = value
        self._tail = (self._tail + 1) % self.capacity()
        self._size += 1

    def write_over(self, value: T) -> None:
        """Enqueue con overwrite: si está lleno, pisa el más viejo."""
        if self.is_full():
            # head == tail en estado full; al escribir, se pierde el elemento más viejo.
            self._buf[self._tail] = value
            self._tail = (self._tail + 1) % self.capacity()
            self._head = self._tail
            # size se mantiene (cap)
            return
        self.write(value)

    def read(self) -> T:
        """Dequeue."""
        if self._size == 0:
            raise IndexError("read from empty RingBuffer")
        v = self._buf[self._head]
        assert v is not None
        self._buf[self._head] = None
        self._head = (self._head + 1) % self.capacity()
        self._size -= 1
        return v

    def to_list(self) -> list[T]:
        """Vista lógica (en orden de lectura)."""
        out: list[T] = []
        cap = self.capacity()
        idx = self._head
        for _ in range(self._size):
            v = self._buf[idx]
            assert v is not None
            out.append(v)
            idx = (idx + 1) % cap
        return out

    def snapshot(self) -> dict[str, object]:
        return {
            "buffer": list(self._buf),
            "head": self._head,
            "tail": self._tail,
            "size": self._size,
            "capacity": self.capacity(),
            "items": self.to_list(),
        }
